from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.gis.geos import Polygon
from django.core import serializers
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import json

from imio_survey.tasks import doSurvey
from imio_survey.models import SurveyType, SurveyTypeLayer, SurveyLayer, SurveyGisServer, SurveyResult

class SurveyTypeView(View):
    def get(self, request, *args, **kwargs):
        result = []
        for st in SurveyType.objects.all():
            result.append({'key': st.key, 'desc': st.description})
        return HttpResponse(json.dumps(result),content_type="application/json")

class SurveyView(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        survey_type = request.POST["st"]
        survey_geom  = request.POST["geom"]
        result = doSurvey(survey_type, survey_geom)
        return HttpResponse(json.dumps(result),content_type="application/json")

    def get(self, request, *args, **kwargs):
        survey_type = request.GET["st"]
        survey_geom  = request.GET["geom"]
        result = doSurvey(survey_type, survey_geom)
        #return HttpResponse(json.dumps(result),content_type="application/json")
        return render(request, 'imio_survey/index.html', {
            'survey_result' : result
        })
