# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

import json

from imio_survey.tasks import doSurvey

class SurveyView(View):
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
