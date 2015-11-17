from django.contrib import admin
from imio_survey.models import SurveyTypeAdmin,SurveyLayerAdmin,SurveyGisServerAdmin

@admin.register(SurveyType)
class SurveyTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(SurveyLayer)
class SurveyLayerAdmin(admin.ModelAdmin):
    pass

@admin.register(SurveyGisServer)
class SurveyGisServerAdmin(admin.ModelAdmin):
    pass
