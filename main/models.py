from django.db import models


class Personnel(models.Model):
    surname = models.CharField('Фамилия', max_length=50)
    name = models.CharField('Имя', max_length=50)
    middleName = models.CharField('Отчество', max_length=50)
    fullname = models.CharField('Полное имя', max_length=50)
    birthDate = models.CharField('Дата рождения', max_length=50)
    phoneNumber = models.CharField('Номер телефона', max_length=50)
    email = models.CharField('Электронная почта', max_length=50)
    dateOfEmployment = models.CharField('Дата трудоустройства', max_length=50)
    structuralDivision = models.CharField('Структурное подразделение', max_length=50)
    department = models.CharField('Отдел', max_length=50)
    heldPost = models.CharField('Должность', max_length=50)

    def __str__(self):
        return self.surname + " " + self.name + " " + self.middleName

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class AdditionalTraining(models.Model):
    personnel = models.ForeignKey(Personnel, related_name='AdditionalTraining', on_delete=models.CASCADE)
    nameOfTraining = models.CharField('Название обучения', max_length=50)
    typeOfTraining = models.CharField('Единоразовое/Регулярное', max_length=50)  # Выпадающий список обязательно
    dateOfCompletionOfTraining = models.CharField('Дата прохождения обучения',
                                                  max_length=50)
    dateOfRepeatedPassageOfTraining = models.CharField('Дата повторного прохождения обучения',
                                                       max_length=50,
                                                       blank=True)

    def __str__(self):
        return self.personnel

    class Meta:
        db_table = "additionalTraining"


class CompulsoryEducation(models.Model):
    personnel = models.ForeignKey(Personnel, related_name='CompulsoryEducation', on_delete=models.CASCADE)
    nameOfTraining = models.CharField('Название обучения', max_length=50)
    typeOfTraining = models.CharField('Единоразовое/Регулярное', max_length=50)  # Выпадающий список обязательно
    dateOfCompletionOfTraining = models.CharField('Дата прохождения обучения',
                                                  max_length=50)
    dateOfRepeatedPassageOfTraining = models.CharField('Дата повторного прохождения обучения',
                                                       max_length=50,
                                                       blank=True)

    def __str__(self):
        return self.personnel

    class Meta:
        db_table = "compulsoryEducation"


class CompulsoryEducationFile(models.Model):
    file = models.FileField(upload_to='documents/')
    compulsoryEducation = models.ForeignKey(CompulsoryEducation, related_name='CompulsoryEducationFile',
                                            on_delete=models.CASCADE)


class AdditionalTrainingFile(models.Model):
    file = models.FileField(upload_to='documents/')
    additionalTraining = models.ForeignKey(AdditionalTraining, related_name='AdditionalTrainingFile',
                                           on_delete=models.CASCADE)


class MedicalExamination(models.Model):
    personnel = models.ForeignKey(Personnel, related_name='MedicalExamination', on_delete=models.CASCADE)
    dateOfMedicalExamination = models.DateField('Дата прохождения медосмотра', max_length=50)  # обязательно
    dateOfRepeatedMedicalExamination = models.DateField('Дата повторного прохождения медосмотра',
                                                        max_length=50)  # обязательно


class Violations(models.Model):
    name = models.CharField('Название нарушения', max_length=50)
    description = models.TextField('Описание нарушения')
    date = models.CharField('Дата нарушения', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Нарушение охраны труда'
        verbose_name_plural = 'Нарушения охраны труда'


class InjuryAccounting(models.Model):
    personnel = models.ForeignKey(Personnel, related_name='InjuryAccounting', on_delete=models.CASCADE)
    name = models.CharField('Название травмы', max_length=50)
    description = models.TextField('Описание травмы')
    date = models.DateField('Дата происшествия')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Учет травм'
        verbose_name_plural = 'Учет травм'


class Documentation(models.Model):
    file = models.FileField('Документ',upload_to='documentation/')


class Testing(models.Model):
    personnel = models.ForeignKey(Personnel, related_name='Testing', on_delete=models.CASCADE)
    typeOfTesting = models.CharField('Вид тестирования', max_length=50)  # !!!
    date = models.DateField('Дата тестирования')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тестирования'
        verbose_name_plural = 'Тестирование'


class Expenses(models.Model):
    name = models.CharField('Название товара', max_length=50)
    date = models.DateField('Дата покупки')
    typeOfTesting = models.IntegerField('Срок годности')
    expiration = models.CharField('Период времени', max_length=50)
    quantity = models.IntegerField('Количество')
    price = models.FloatField('Цена', max_length=50)
    cost = models.FloatField('Стоимость', max_length=50)
    invoice = models.FileField('Накладная', upload_to='invoice/')  # Загрузить накладную

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Затраты'
        verbose_name_plural = 'Затрата'


class Orders(models.Model):
    expenses = models.ForeignKey(Expenses, related_name='Orders', on_delete=models.CASCADE)  # !!!
    typeOfTesting = models.IntegerField('Количество')
    date = models.DateField('Дата выдачи')
    department = models.CharField('Отдел', max_length=50)
    personnel = models.ForeignKey(Personnel, related_name='Orders', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказ'


class EquipmentAccounting(models.Model):
    name = models.CharField('Наименование', max_length=50)
    equipmentPassport = models.FileField('Паспорт оборудования', upload_to='equipmentPassport/')  # паспорт оборудования
    dateOfCommissioning = models.DateField('Дата введения в эксплуатацию')
    dateOfTechnicalInspection = models.DateField('Дата проведения тех обследования')
    dateOfPlannedTechnicalInspection = models.DateField('Дата планируемого проведения тех обследования')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Учет оборудования'
        verbose_name_plural = 'Учет оборудования'
