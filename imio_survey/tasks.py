# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task
from celery import chord
from celery.utils.log import get_task_logger
from celery.result import AsyncResult

from django.db import transaction

from django.contrib.gis.geos import GEOSGeometry, fromstr

from imio_survey.models import SurveyType, SurveyTypeLayer, SurveyLayer, SurveyGisServer
from imio_survey.queriers.factories import SurveyQuerierFactory

logger = get_task_logger(__name__)

@shared_task(ignore_result=False)
def mul(x, y):
    return x * y

@shared_task(ignore_result=False)
def mergeResults(results):
    return results

@shared_task(ignore_result=False)
def queryLayer(layer_pk, wktGeometry, buffer):
    geosGeom = fromstr(wktGeometry)
    geosGeomBuffer = geosGeom.buffer(buffer)
    layer = SurveyLayer.objects.get(pk = layer_pk)
    gis_server = layer.gis_server
    querier = SurveyQuerierFactory().createQuerier(gis_server.servertype)
    result = querier.identify(geosGeomBuffer, layer.layer_name, gis_server.url)
    return result

def doSurvey(surveyTypekey,wktGeometry):
    #TODO Handle surveynotfound
    #TODO EagerLoad every layer and membership to avoid n+1 select
    #TODO Check geometry validity
    st = SurveyType.objects.get(pk = surveyTypekey)
    job = chord((queryLayer.s(sl.pk,wktGeometry,SurveyTypeLayer.objects.get(survey_type=st,survey_layer=sl).buffer) for sl in st.survey_layers.all()))(mergeResults.s())

    #TODO Set timeout value as a parameter
    result = job.get(timeout=15)
    if job.successful():
        return result
    else:
        return None
