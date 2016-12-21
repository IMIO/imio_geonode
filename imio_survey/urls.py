# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from imio_survey.views.survey import SurveyView
from imio_survey.views.surveytype import SurveyTypeView, SurveyTypeLayersView
from imio_survey.views.surveyvalues import SurveyValuesView

urlpatterns = [
    url(r'^$', csrf_exempt(SurveyView.as_view()), name='index'),
    url(r'survey_type_list', SurveyTypeView.as_view(), name='survey_type_list'),
    url(r'survey_type_layers', SurveyTypeLayersView.as_view(), name='survey_type_layers'),
    url(r'survey_value_list', SurveyValuesView.as_view(), name='survey_value_list'),
]
