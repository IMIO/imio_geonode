# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from imio_survey.views import SurveyView, SurveyTypeView


urlpatterns = [
    url(r'^$', csrf_exempt(SurveyView.as_view()), name='index'),
    url(r'survey_type_list', SurveyTypeView.as_view(), name='survey_type_list'),
]
