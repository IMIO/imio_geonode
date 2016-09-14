# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import shared_task
from celery import chord
from celery.utils.log import get_task_logger
from celery.result import AsyncResult

from django.db import transaction
from django.contrib.gis.geos import GEOSGeometry, fromstr
from imio_survey.models import SurveyType, SurveyTypeLayer, SurveyLayer, SurveyGisServer, SurveyResult
from imio_survey.queriers.factories import SurveyQuerierFactory

import urllib2

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
    logger.info("Querying layer %s (%s)" % (layer.description, layer.layer_name))
    gis_server = layer.gis_server
    query_result = { 'layer_id' : layer.id , 'description': layer.description, 'name': layer.layer_name, 'attributes': None, 'success' : False, 'message': None}
    try:
        querier = SurveyQuerierFactory().createQuerier(gis_server.servertype)
        result = querier.identify(geosGeomBuffer,layer.geometry_field_name, layer.layer_name, gis_server.url, gis_server.username, gis_server.password)
        query_result['attributes'] = result
        query_result['success'] = True
    except urllib2.HTTPError, error:
        query_result['success'] = False
        query_result['message'] = "HTTPError : " + str(error.code) + error.filename
        print("ERROR: ", error.read())
    except Exception as ex:
        query_result['success'] = False
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex), ex.args)
        query_result['message'] = message
    return query_result

def doSurvey(surveyTypekey,wktGeometry):
    #TODO EagerLoad every layer and membership to avoid n+1 select
    #TODO Check geometry validity
    logger.info("Geom : %s" % wktGeometry)
    #TODO Check if surveytype exist
    st = SurveyType.objects.get(pk = surveyTypekey)
    MAX_RETRIES_CHORD=30
    CHORD_INTERVAL=1
    queries= [queryLayer.s(sl.pk,wktGeometry,SurveyTypeLayer.objects.get(survey_type=st,survey_layer=sl).buffer) for sl in st.survey_layers.all() ]
    merger=mergeResults.s()
    #job = chord((queryLayer.s(sl.pk,wktGeometry,SurveyTypeLayer.objects.get(survey_type=st,survey_layer=sl).buffer) for sl in st.survey_layers.all()))(mergeResults.s())
    job = chord(
        header=queries,
        body =merger).apply_async(max_retries=MAX_RETRIES_CHORD, interval=CHORD_INTERVAL)

    #TODO Set timeout value as a parameter
    #TODO Catch TimouOut error
    result = job.get(timeout=30)
    if job.successful():
        return result
    else:
        return None
