# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger

from django.db import transaction

from django.contrib.gis.geos import GEOSGeometry, fromstr

from imio_survey.models import SurveyType, SurveyTypeLayer, SurveyLayer, SurveyGisServer
from imio_survey.queriers.factories import SurveyQuerierFactory

logger = get_task_logger(__name__)

@shared_task
def mul(x, y):
    return x * y

@shared_task
def doSurvey(surveyTypekey,wktGeometry):
    #TODO Handle surveynotfound
    #TODO EagerLoad every layer and membership to avoid n+1 select
    #TODO Check geometry validity
    surveyType = SurveyType.objects.get(pk = surveyTypekey)
    results = []
    #TODO Check Error for querylayer and invalidate the survey if any
    for survey_layer in surveyType.survey_layers.all():
        surveyTypeLayer = SurveyTypeLayer.objects.get(survey_type = surveyType, survey_layer = survey_layer)
        result = queryLayer.delay(survey_layer.pk, wktGeometry, surveyTypeLayer.buffer)
        results.append(result)
    return results

@shared_task
def queryLayer(layer_pk, wktGeometry, buffer):
    geosGeom = fromstr(wktGeometry)
    geosGeomBuffer = geosGeom.buffer(buffer)
    layer = SurveyLayer.objects.get(pk = layer_pk)
    gis_server = layer.gis_server
    querier = SurveyQuerierFactory().createQuerier(gis_server.servertype)
    result = querier.identify(geometry, layers, url)
    return result
