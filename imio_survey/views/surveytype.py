# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.generic import View

from imio_survey.models import SurveyType

import json

class SurveyTypeView(View):
    def get(self, request, *args, **kwargs):
        """ Get List of available surveys """
        result = []
        for st in SurveyType.objects.all():
            result.append({'key': st.key, 'desc': st.description})
        return HttpResponse(json.dumps(result),content_type="application/json")

class SurveyTypeLayersView(View):
    def get(self, request, *args, **kwargs):
        """ Get List of available layer for a given survey """
        survey_type_param = request.GET.get("st", None) #SurveyType
        survey_type_obj = SurveyType.objects.get(pk= survey_type_param)
        result = []
        for layer in survey_type_obj.survey_layers.all():
            result.append({
                'l': layer.id,
                'desc': layer.description,
                'geom': layer.geometry_field_name
            })
        return HttpResponse(json.dumps(result),content_type="application/json")
