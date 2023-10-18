import calendar
import datetime
import json
import time
from dateutil.relativedelta import relativedelta

from django.db import transaction, IntegrityError
from django.db.models import Count, Sum
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from qsstats import QuerySetStats

from .forms import PersonnelForm, CompulsoryEducationForm, AdditionalTrainingForm, MedicalExaminationForm, \
    ViolationsForm, InjuryAccountingForm, DocumentationForm, TestingForm, ExpensesForm, OrdersForm, \
    EquipmentAccountingForm
from .models import Personnel, CompulsoryEducationFile, CompulsoryEducation, AdditionalTraining, AdditionalTrainingFile, \
    MedicalExamination, Violations, InjuryAccounting, Documentation, Testing, Expenses, Orders, EquipmentAccounting


def index(request):
    # сортировка по полю ид
    # person = Personnel.objects.order_by('id')
    # сортировка по полю ид в обратном порядке + срез выбираем только первые 1 эл
    # person = Personnel.objects.order_by('-id')[:1]
    person = Personnel.objects.all()
    file = CompulsoryEducationFile.objects.select_related().all()
    if request.method == "POST":
        print(request.POST.get('value'))
        idcard = request.POST.get('value')
        return redirect('card', idcard=idcard)
    return render(request, 'main/index.html', {'title': 'Главная страница сайта',
                                               'person': person,
                                               'file': file
                                               })


def addPerson(request):
    context = {}
    CompulsoryEducationFormset = modelformset_factory(CompulsoryEducation, form=CompulsoryEducationForm)
    formset = CompulsoryEducationFormset(request.POST or None, queryset=CompulsoryEducation.objects.none(),
                                         prefix='compulsoryEducation')
    AdditionalTrainingFormset = modelformset_factory(AdditionalTraining, form=AdditionalTrainingForm)
    additionalTrainingFormset = AdditionalTrainingFormset(request.POST or None,
                                                          queryset=AdditionalTraining.objects.none(),
                                                          prefix='additionalTraining')
    medicalExaminationForm = MedicalExaminationForm(request.POST or None)
    form = PersonnelForm(request.POST or None)
    if request.method == "POST" and "save" in request.POST:
        form = PersonnelForm(request.POST)
        files = request.FILES
        fileskeys = [*files.keys()]
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    personnel = form.save(commit=False)
                    personnel.fullname = personnel.surname + " " + personnel.name + " " + personnel.middleName
                    personnel.save()
                    medicalExamination = medicalExaminationForm.save(commit=False)
                    medicalExamination.personnel = personnel
                    medicalExamination.save()
                    filterfileskeys = [s for s in fileskeys if 'compulsoryEducation' in s]
                    zipform = zip(formset, filterfileskeys)
                    for compulsoryEducation, fileskey in zipform:
                        print(fileskey)
                        data = compulsoryEducation.save(commit=False)
                        data.personnel = personnel
                        data.save()
                        filesvalue = files.getlist(fileskey)
                        print(filesvalue)
                        for f in filesvalue:
                            fl = CompulsoryEducationFile(compulsoryEducation=data, file=f)
                            fl.save()
                    filterfileskeys = [s for s in fileskeys if 'additionalTraining' in s]
                    zipform = zip(additionalTrainingFormset, filterfileskeys)
                    for additionalTraining, fileskey in zipform:
                        data = additionalTraining.save(commit=False)
                        data.personnel = personnel
                        data.save()
                        filesvalue = files.getlist(fileskey)
                        for f in filesvalue:
                            fl = AdditionalTrainingFile(additionalTraining=data, file=f)
                            fl.save()
            except IntegrityError:
                print("Error Encountered")
            return redirect('home')
    if request.method == "POST" and "cancel" in request.POST:
        return redirect('home')
    now = datetime.datetime.now()
    num_days = calendar.monthrange(now.year, now.month)
    scheduledateOfMedicalExamination = MedicalExamination.objects.filter(dateOfMedicalExamination__year=now.year,
                                                                         dateOfMedicalExamination__month=now.month)
    scheduledateOfRepeatedMedicalExamination = MedicalExamination.objects.filter(
        dateOfRepeatedMedicalExamination__year=now.year,
        dateOfRepeatedMedicalExamination__month=now.month)
    schedule = dict()
    for item in scheduledateOfMedicalExamination:
        if schedule.get(item.dateOfMedicalExamination):
            if not (item.personnel.fullname in schedule.get(item.dateOfMedicalExamination)):
                schedule.setdefault(item.dateOfMedicalExamination, []).append(item.personnel.fullname)
        else:
            schedule.setdefault(item.dateOfMedicalExamination, []).append(item.personnel.fullname)
    for item in scheduledateOfRepeatedMedicalExamination:
        if schedule.get(item.dateOfMedicalExamination):
            if not (item.personnel.fullname + " (повторно)" in schedule.get(item.dateOfMedicalExamination)):
                schedule.setdefault(item.dateOfMedicalExamination, []).append(item.personnel.fullname + " (повторно)")
        else:
            schedule.setdefault(item.dateOfMedicalExamination, []).append(item.personnel.fullname + " (повторно)")
    context['medicalExaminationForm'] = medicalExaminationForm
    context['additionalTrainingFormset'] = additionalTrainingFormset
    context['form'] = form
    context['formset'] = formset
    # context['schedule'] = schedule
    return render(request, 'main/addPerson.html', context)


def card(request, idcard):
    context = {}
    person = Personnel.objects.get(pk=idcard)
    compulsoryEducation = CompulsoryEducation.objects.filter(personnel_id=int(idcard))
    compulsoryEducationFiles = {}
    for item in compulsoryEducation:
        compulsoryEducationFile = CompulsoryEducationFile.objects.filter(compulsoryEducation_id=int(item.id))
        compulsoryEducationFiles[item.id] = compulsoryEducationFile
    additionalTraining = AdditionalTraining.objects.filter(personnel_id=int(idcard))
    additionalTrainingFiles = {}
    for item in additionalTraining:
        additionalTrainingFile = AdditionalTrainingFile.objects.filter(additionalTraining_id=int(item.id))
        additionalTrainingFiles[item.id] = additionalTrainingFile
    medicalExamination = MedicalExamination.objects.filter(personnel_id=int(idcard))
    context['title'] = 'Карточка сотрудника'
    context['person'] = person
    context['compulsoryEducation'] = compulsoryEducation
    context['compulsoryEducationFiles'] = compulsoryEducationFiles
    context['additionalTrainingFiles'] = additionalTrainingFiles
    context['additionalTraining'] = additionalTraining
    context['medicalExamination'] = medicalExamination

    return render(request, 'main/card.html', context)


def registerOfViolations(request):
    violations = Violations.objects.all()
    if request.method == "POST":
        idcard = request.POST.get('value')
        return redirect('cardRegisterOfViolations', idcard=idcard)
    return render(request, 'main/registerOfViolations.html', {'title': 'Реестр нарушений',
                                                              'violations': violations
                                                              })


def addRegisterOfViolations(request):
    context = {}
    form = ViolationsForm(request.POST or None)
    if request.method == "POST" and "save" in request.POST:
        form = ViolationsForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    violations = form.save(commit=False)
                    violations.save()
            except IntegrityError:
                print("Error Encountered")
            return redirect('registerOfViolations')
    if "cancel" in request.POST:
        return redirect('registerOfViolations')
    context['form'] = form
    return render(request, 'main/addRegisterOfViolations.html', context)


def cardRegisterOfViolations(request, idcard):
    context = {}
    violations = Violations.objects.get(pk=idcard)
    context['title'] = 'Карточка нарушения'
    context['violations'] = violations
    return render(request, 'main/cardRegisterOfViolations.html', context)


def injuryAccounting(request):
    accountingForInjuries = InjuryAccounting.objects.all()
    context = {}
    if accountingForInjuries:
        start_date = (InjuryAccounting.objects.order_by('date')[0]).date
        end_date = (InjuryAccounting.objects.order_by('-date')[0]).date  # + datetime.timedelta(days=days)
        qsstats = QuerySetStats(accountingForInjuries, date_field='date', aggregate=Count('id'))
        valuesdays = qsstats.time_series(start_date, end_date, interval='days')
        valuesmonths = qsstats.time_series(start_date, end_date, interval='months')
        valuesyears = qsstats.time_series(start_date, end_date.replace(year=end_date.year + 1), interval='years')
        context['valuesdays'] = valuesdays
        context['valuesmonths'] = valuesmonths
        context['valuesyears'] = valuesyears
        print(valuesmonths)
        print(valuesyears)
    if request.method == "POST":
        idcard = request.POST.get('value')
        return redirect('cardAccountingForInjuries', idcard=idcard)
    context['accountingForInjuries'] = accountingForInjuries
    return render(request, 'main/accountingForInjuries.html', context)


def addInjuryAccounting(request):
    context = {}
    form = InjuryAccountingForm(request.POST or None)
    if request.method == "POST" and "save" in request.POST:
        print(request.POST)
        form = InjuryAccountingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # your_date = datetime.date(2015, 12, 1)
                    injuryAccounting = form.save(commit=False)
                    pers = Personnel.objects.get(fullname=request.POST.get("personnel"))
                    injuryAccounting.personnel = pers
                    # injuryAccounting.date=your_date
                    injuryAccounting.save()
            except IntegrityError:
                print("Error Encountered")
            return redirect('accountingForInjuries')
    if "cancel" in request.POST:
        return redirect('accountingForInjuries')
    context['form'] = form
    return render(request, 'main/addAccountingForInjuries.html', context)


def cardInjuryAccounting(request, idcard):
    context = {}
    injuryAccounting = InjuryAccounting.objects.get(pk=idcard)
    context['title'] = 'Карточка нарушения'
    context['injuryAccounting'] = injuryAccounting
    return render(request, 'main/cardAccountingForInjuries.html', context)


def monitoring(request):
    return render(request, 'main/monitoring.html')


def testing(request):
    context = {}
    testing = Testing.objects.all()
    context['testing'] = testing
    return render(request, 'main/testing/testing.html', context)


def addTesting(request):
    context = {}
    form = TestingForm(request.POST or None)
    if request.method == "POST" and "save" in request.POST:
        print(request.POST)
        form = TestingForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    testing = form.save(commit=False)
                    pers = Personnel.objects.get(fullname=request.POST.get("personnel"))
                    testing.personnel = pers
                    testing.save()
            except IntegrityError:
                print("Error Encountered")
            return redirect('testing')
    if "cancel" in request.POST:
        return redirect('testing')
    context['form'] = form
    return render(request, 'main/testing/addTesting.html', context)


def expenses(request):
    context = {}
    expenses = Expenses.objects.all()
    context['expenses'] = expenses
    if expenses:
        start_date = (Expenses.objects.order_by('date')[0]).date
        end_date = (Expenses.objects.order_by('-date')[0]).date  # + datetime.timedelta(days=days)
        qsstats = QuerySetStats(expenses, date_field='date', aggregate=Sum('cost'))
        valuesmonths = qsstats.time_series(start_date.replace(month=start_date.month - 1),
                                           end_date.replace(month=end_date.month + 1), interval='months')
        valuesyears = qsstats.time_series(start_date.replace(year=start_date.year - 1),
                                          end_date.replace(year=end_date.year + 1), interval='years')
        for index, item in enumerate(valuesmonths):
            if item[1] == 'None' or item[1] == None:
                valuesmonths[index] = (item[0], 0)
            else:
                valuesmonths[index] = (item[0], str(item[1]).replace(',', '.'))
        for index, item in enumerate(valuesyears):
            if item[1] == 'None' or item[1] == None:
                valuesyears[index] = (item[0], 0)
            else:
                valuesyears[index] = (item[0], str(item[1]).replace(',', '.'))
        print(start_date)
        print(end_date)
        context['valuesmonths'] = valuesmonths
        context['valuesyears'] = valuesyears
    return render(request, 'main/expenses/expenses.html', context)


def addExpenses(request):
    context = {}
    form = ExpensesForm(request.POST, request.FILES)
    if request.method == "POST" and "save" in request.POST:
        form = ExpensesForm(request.POST, request.FILES)
        if form.is_valid():
            expenses = form.save(commit=False)
            expenses.cost = float(expenses.price) * int(expenses.quantity)
            expenses.save()
            form.save()
            return redirect('expenses')
    if "cancel" in request.POST:
        return redirect('expenses')
    context['form'] = form
    return render(request, 'main/expenses/addExpenses.html', context)


def orders(request):
    context = {}
    orders = Orders.objects.all()
    context['orders'] = orders

    now = datetime.date.today()

    delay = []
    soon = []
    expenses = Expenses.objects.all()
    for exp in expenses:
        fin = exp.date
        if exp.expiration == "Дней":
            fin = exp.date + relativedelta(day=+exp.typeOfTesting)
        if exp.expiration == "Месяцев":
            fin = exp.date + relativedelta(months=+exp.typeOfTesting)
        if exp.expiration == "Лет":
            fin = exp.date + relativedelta(year=+exp.typeOfTesting)
        a = fin - now
        if a.days < 0:
            delay.append(exp)
        elif a.days < 30:
            soon.append(exp)
    context['delay'] = delay
    context['soon'] = soon
    context['expenses'] = expenses
    return render(request, 'main/orders/orders.html', context)


def addOrders(request):
    context = {}
    form = OrdersForm(request.POST)
    if request.method == "POST" and "save" in request.POST:
        form = OrdersForm(request.POST)
        if form.is_valid():
            orders = form.save(commit=False)
            # expenses.cost = float(expenses.price) * int(expenses.quantity)
            expenses = Expenses.objects.get(name=request.POST.get("expenses"))
            # expenses = request.POST.get("expenses")
            if request.POST.get("personnel"):
                pers = Personnel.objects.get(fullname=request.POST.get("personnel"))
                orders.personnel = pers
                orders.department = pers.department
            orders.expenses = expenses
            orders.save()
            form.save()
            return redirect('orders')
    if "cancel" in request.POST:
        return redirect('orders')
    context['form'] = form
    return render(request, 'main/orders/addOrders.html', context)


def equipmentAccounting(request):
    context = {}
    equipmentAccounting = EquipmentAccounting.objects.all()
    context['equipmentAccounting'] = equipmentAccounting
    return render(request, 'main/equipmentAccounting/equipmentAccounting.html', context)


def addEquipmentAccounting(request):
    context = {}
    form = EquipmentAccountingForm(request.POST, request.FILES)
    if request.method == "POST" and "save" in request.POST:
        form = EquipmentAccountingForm(request.POST, request.FILES)
        if form.is_valid():
            equipmentAccounting = form.save(commit=False)
            equipmentAccounting.save()
            form.save()
            return redirect('equipmentAccounting')
    if "cancel" in request.POST:
        return redirect('equipmentAccounting')
    context['form'] = form
    return render(request, 'main/equipmentAccounting/addEquipmentAccounting.html',context)


def documentation(request):
    documentation = Documentation.objects.all()
    form = DocumentationForm()
    if request.method == 'POST':
        files = request.FILES
        for f in files.getlist('file'):
            el = Documentation()
            el.file = f
            el.save()
    return render(request, 'main/documentation.html', {'documentation': documentation,
                                                       'form': form})


@csrf_exempt
def ajax_view_technicalExaminations(request):
    num = request.session.get('num')
    if request.method == 'POST':
        print(request.POST.get('serialized-data'))
        print(int(request.POST.get('serialized-data')))
        now = datetime.date.today()
        num_days = calendar.monthrange(now.year, now.month)
        now = datetime.date.today() + relativedelta(months=+int(request.POST.get('serialized-data')))
        year = now.year
        month = now.month
        num_days = calendar.monthrange(year, month)
        print(year)
        print(month)
        period = 'Начало периода : 01.' + str(month) + '.' + str(year) + '<br>' + 'Конец периода : ' + str(
            num_days[1]) + '.' + str(month) + '.' + str(year) + '.'
        scheduledateOfMedicalExamination = EquipmentAccounting.objects.filter(dateOfTechnicalInspection__year=year,
                                                                              dateOfTechnicalInspection__month=month)
        scheduledateOfRepeatedMedicalExamination = EquipmentAccounting.objects.filter(
            dateOfPlannedTechnicalInspection__year=year,
            dateOfPlannedTechnicalInspection__month=month)
        schedule = dict()
        for item in scheduledateOfMedicalExamination:
            if schedule.get(item.dateOfTechnicalInspection):
                if not (item.name in schedule.get(item.dateOfTechnicalInspection)):
                    schedule.setdefault(item.dateOfTechnicalInspection, []).append(item.name)
            else:
                schedule.setdefault(item.dateOfTechnicalInspection, []).append(item.name)

        for item in scheduledateOfRepeatedMedicalExamination:
            if schedule.get(item.dateOfPlannedTechnicalInspection):
                if not (item.name + " (планируемое тех обследование)" in schedule.get(
                        item.dateOfPlannedTechnicalInspection)):
                    schedule.setdefault(item.dateOfPlannedTechnicalInspection, []).append(
                        item.name + " (планируемое тех обследование)")
            else:
                schedule.setdefault(item.dateOfPlannedTechnicalInspection, []).append(
                    item.name + "  (планируемое тех обследование)")
        html = ''
        print(schedule)
        if not len(schedule) == 0:
            for key in schedule:
                html += '<tr><td>' + key.strftime("%m/%d/%Y") + '</td><td>'
                for name in schedule.get(key):
                    html += '<li>' + name + '</li>'
                html += '</td></tr>'
        else:
            html += '<h5 class="mb-3">Записи отсутсвуют!</h5>'
        response_data = {}
        response_data['num'] = num
        response_data['html'] = html
        response_data['period'] = period

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )


@csrf_exempt
def ajax_view_testing(request):
    num = request.session.get('num')
    if request.method == 'POST':
        # now = datetime.date.today()
        # num_days = calendar.monthrange(now.year, now.month)
        now = datetime.date.today() + relativedelta(months=+int(request.POST.get('serialized-data')))
        year = now.year
        month = now.month
        num_days = calendar.monthrange(year, month)
        period = 'Начало периода : 01.' + str(month) + '.' + str(year) + '<br>' + 'Конец периода : ' + str(
            num_days[1]) + '.' + str(month) + '.' + str(year) + '.'
        date = Testing.objects.filter(date__year=year, date__month=month)
        schedule = dict()
        for item in date:
            if schedule.get(item.date):
                if not (item.personnel.fullname in schedule.get(item.date)):
                    schedule.setdefault(item.date, []).append(item.personnel.fullname)
            else:
                schedule.setdefault(item.date, []).append(item.personnel.fullname)
        html = ''
        print(schedule)
        if not len(schedule) == 0:
            for key in schedule:
                html += '<tr><td>' + key.strftime("%m/%d/%Y") + '</td><td>'
                for name in schedule.get(key):
                    html += '<li>' + name + '</li>'
                html += '</td></tr>'
        else:
            html += '<h5 class="mb-3">Записи отсутсвуют!</h5>'
        response_data = {}
        response_data['num'] = num
        response_data['html'] = html
        response_data['period'] = period

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )


@csrf_exempt
def ajax_view(request):
    num = request.session.get('num')
    if request.method == 'POST':
        print(request.POST.get('serialized-data'))
        print(int(request.POST.get('serialized-data')))
        now = datetime.date.today()
        num_days = calendar.monthrange(now.year, now.month)
        now = datetime.date.today() + relativedelta(months=+int(request.POST.get('serialized-data')))
        year = now.year
        month = now.month
        num_days = calendar.monthrange(year, month)
        print(year)
        print(month)
        period = 'Начало периода : 01.' + str(month) + '.' + str(year) + '<br>' + 'Конец периода : ' + str(
            num_days[1]) + '.' + str(month) + '.' + str(year) + '.'
        scheduledateOfMedicalExamination = MedicalExamination.objects.filter(dateOfMedicalExamination__year=year,
                                                                             dateOfMedicalExamination__month=month)
        scheduledateOfRepeatedMedicalExamination = MedicalExamination.objects.filter(
            dateOfRepeatedMedicalExamination__year=year,
            dateOfRepeatedMedicalExamination__month=month)
        schedule = dict()
        for item in scheduledateOfMedicalExamination:
            if schedule.get(item.dateOfMedicalExamination):
                if not (item.personnel.fullname in schedule.get(item.dateOfMedicalExamination)):
                    schedule.setdefault(item.dateOfMedicalExamination, []).append(item.personnel.fullname)
            else:
                schedule.setdefault(item.dateOfMedicalExamination, []).append(item.personnel.fullname)

        for item in scheduledateOfRepeatedMedicalExamination:
            if schedule.get(item.dateOfRepeatedMedicalExamination):
                if not (item.personnel.fullname + " (повторно)" in schedule.get(item.dateOfRepeatedMedicalExamination)):
                    schedule.setdefault(item.dateOfRepeatedMedicalExamination, []).append(
                        item.personnel.fullname + " (повторно)")
            else:
                schedule.setdefault(item.dateOfRepeatedMedicalExamination, []).append(
                    item.personnel.fullname + " (повторно)")
        html = ''
        print(schedule)
        if not len(schedule) == 0:
            for key in schedule:
                html += '<tr><td>' + key.strftime("%m.%d.%Y") + '</td><td>'
                for name in schedule.get(key):
                    html += '<li>' + name + '</li>'
                html += '</td></tr>'
        else:
            html += '<h5 class="mb-3">Записи отсутсвуют!</h5>'
        response_data = {}
        response_data['num'] = num
        response_data['html'] = html
        response_data['period'] = period

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )


def email_autocomplete(request):
    if request.GET.get('q'):
        q = request.GET['q']
        data = Personnel.objects.filter(fullname__contains=q).values_list('fullname', flat=True)
        json = list(data)
        return JsonResponse(json, safe=False)
    else:
        HttpResponse("No cookies")


def expenses_autocomplete(request):
    if request.GET.get('q'):
        q = request.GET['q']
        data = Expenses.objects.filter(name__contains=q).values_list('name', flat=True)
        json = list(data)
        return JsonResponse(json, safe=False)
    else:
        HttpResponse("No cookies")


def aboba(request):
    return render(request, 'main/aboba.html')
