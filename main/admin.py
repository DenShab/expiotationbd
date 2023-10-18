from django.contrib import admin
from .models import Personnel, CompulsoryEducationFile, AdditionalTraining, CompulsoryEducation, AdditionalTrainingFile

admin.site.register(
    [Personnel, CompulsoryEducationFile, AdditionalTraining, CompulsoryEducation, AdditionalTrainingFile])
