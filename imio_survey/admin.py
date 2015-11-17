from django.contrib import admin
from imio_survey.models import SurveyType,SurveyLayer,SurveyGisServer,SurveyTypeLayer

class SurveyTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(SurveyType, SurveyTypeAdmin)

class SurveyLayerAdmin(admin.ModelAdmin):
    pass
admin.site.register(SurveyLayer, SurveyLayerAdmin)

class SurveyGisServerAdmin(admin.ModelAdmin):
    pass
admin.site.register(SurveyGisServer, SurveyGisServerAdmin)

class SurveyTypeLayerAdmin(admin.ModelAdmin):
    pass
admin.site.register(SurveyTypeLayer, SurveyTypeLayerAdmin)
