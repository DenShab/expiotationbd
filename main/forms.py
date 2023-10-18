from django.forms import ModelForm, TextInput, FileInput, Select, ClearableFileInput, FileField, Textarea, NumberInput
from django import forms
from .models import *


class PersonnelForm(ModelForm):
    class Meta:
        model = Personnel
        fields = ["surname", "name", "middleName", "birthDate",
                  "phoneNumber", "email", "dateOfEmployment", "structuralDivision",
                  "department", "heldPost"]
        widgets = {
            "surname": TextInput(
                attrs={"class": "form-control"}
            ),
            "name": TextInput(
                attrs={"class": "form-control"}
            ),
            "middleName": TextInput(
                attrs={"class": "form-control"}
            ),
            "birthDate": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            ),
            "phoneNumber": TextInput(
                attrs={"class": "form-control",
                       "type": "tel"}
            ),
            "email": TextInput(
                attrs={"class": "form-control",
                       "type": "email"}
            ),
            "dateOfEmployment": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            ),
            "structuralDivision": TextInput(
                attrs={"class": "form-control"}
            ),
            "department": TextInput(
                attrs={"class": "form-control"}
            ),
            "heldPost": TextInput(
                attrs={"class": "form-control"}
            )
        }


class ViolationsForm(ModelForm):
    class Meta:
        model = Violations
        fields = ["name", "description", "date"]
        widgets = {
            "name": TextInput(
                attrs={"class": "form-control"}
            ),
            "description": Textarea(
                attrs={"class": "form-control"}
            ),
            "date": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            ),

        }


class AutoCompleteSelectMultipleField(object):
    pass


class InjuryAccountingForm(ModelForm):
    class Meta:
        model = InjuryAccounting
        fields = ["name", "description", "date", ]
        title = forms.CharField(max_length=255)
        widgets = {
            "name": TextInput(
                attrs={"class": "form-control"}
            ),
            "description": Textarea(
                attrs={"class": "form-control"}
            ),
            "date": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            ),

        }


class MedicalExaminationForm(ModelForm):
    class Meta:
        model = MedicalExamination
        fields = ["dateOfMedicalExamination", "dateOfRepeatedMedicalExamination"]
        widgets = {
            "dateOfMedicalExamination": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            ),
            "dateOfRepeatedMedicalExamination": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            ),

        }


class CompulsoryEducationFileForm(ModelForm):
    class Meta:
        model = CompulsoryEducationFile
        fields = ['file']
        widgets = {
            'file': FileInput(attrs={'enctype': "multipart/form-data",
                                     'аallow_multiple_selected':True}),
        }


class AdditionalTrainingFileFileForm(ModelForm):
    class Meta:
        model = AdditionalTrainingFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'class': 'formset-field'}),
        }


class CompulsoryEducationForm(ModelForm):
    files = FileField(widget=ClearableFileInput(attrs={ 'class': 'formset-field',
                                     'аallow_multiple_selected':True}), required=False)

    class Meta:
        model = CompulsoryEducation
        fields = [
            'nameOfTraining',
            'typeOfTraining',
            'dateOfCompletionOfTraining',
            'dateOfRepeatedPassageOfTraining'
        ]
        widgets = {
            "nameOfTraining": TextInput(
                attrs={'class': 'formset-field'}
            ),
            "typeOfTraining": Select(
                attrs={'class': 'formset-field'},
                choices=[('1', 'Единоразовое'), ('2', 'Регулярное')]
            ),
            "dateOfCompletionOfTraining": TextInput(
                attrs={'class': 'formset-field',
                       "type": "date"}
            ),
            "dateOfRepeatedPassageOfTraining": TextInput(
                attrs={'class': 'formset-field',
                       "type": "date"}
            ), }


class AdditionalTrainingForm(ModelForm):
    files = FileField(widget=ClearableFileInput(attrs={'class': 'formset-field',
                                     'аallow_multiple_selected':True}), required=False)

    class Meta:
        model = AdditionalTraining
        fields = ['nameOfTraining', 'typeOfTraining', 'dateOfCompletionOfTraining', 'dateOfRepeatedPassageOfTraining']
        widgets = {
            "nameOfTraining": TextInput(
                attrs={"class": "formset-field"}
            ),
            "typeOfTraining": Select(
                attrs={"class": "formset-field"},
                choices=[('1', 'Единоразовое'), ('2', 'Регулярное')]
            ),
            "dateOfCompletionOfTraining": TextInput(
                attrs={"class": "formset-field",
                       "type": "date"}
            ),
            "dateOfRepeatedPassageOfTraining": TextInput(
                attrs={"class": "formset-field",
                       "type": "date"}
            ), }


class DocumentationForm(ModelForm):
    class Meta:
        model = Documentation
        fields = ['file']
        widgets = {
            'file': FileInput(attrs={'enctype': "multipart/form-data",
                                     'аallow_multiple_selected':True}),
        }


class TestingForm(ModelForm):
    class Meta:
        model = Testing
        fields = ["typeOfTesting", "date"]
        widgets = {
            "typeOfTesting": Select(
                attrs={'class': 'formset-field'},
                choices=[('Тестирование', 'Тестирование'), ('Охрана труда А1', 'Охрана труда А1'), (' ', ' ')]
            ),
            "date": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            ),
        }


class ExpensesForm(ModelForm):
    class Meta:
        model = Expenses
        fields = ["name", "date", "typeOfTesting", "expiration", "quantity", "price", "invoice"]
        widgets = {
            "name": TextInput(
                attrs={"class": "form-control"}
            ),
            "date": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            ),
            "typeOfTesting": NumberInput(
                attrs={"class": "form-control"}
            ),
            "expiration": Select(
                attrs={'class': 'formset-field'},
                choices=[('Дней', 'Дней'), ('Месяцев', 'Месяцев'), ('Лет', 'Лет')]
            ),
            "quantity": NumberInput(
                attrs={"class": "form-control"}
            ),
            "price": NumberInput(
                attrs={"class": "form-control",
                       'step': "0.01"}
            ),
            'invoice': FileInput(attrs={'enctype': "multipart/form-data",
                                     'аallow_multiple_selected':True}),

        }


class EquipmentAccountingForm(ModelForm):
    class Meta:
        model = EquipmentAccounting
        fields = ["name", "equipmentPassport", "dateOfCommissioning", "dateOfTechnicalInspection",
                  "dateOfPlannedTechnicalInspection"]
        widgets = {
            "name": TextInput(
                attrs={"class": "form-control"}
            ),
            'equipmentPassport': FileInput(attrs={'enctype': "multipart/form-data",
                                     'аallow_multiple_selected':True}),

            "dateOfCommissioning": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            ),
            "dateOfTechnicalInspection": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            ),
            "dateOfPlannedTechnicalInspection": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            )
        }


class OrdersForm(ModelForm):
    class Meta:
        model = Orders
        fields = ["typeOfTesting", "date", "department"]
        widgets = {
            'typeOfTesting': NumberInput(
                attrs={"class": "form-control"}
            ),
            "date": TextInput(
                attrs={"class": "form-control",
                       "type": "date"}
            ),
            "department": TextInput(
                attrs={"class": "form-control"}
            )
        }
