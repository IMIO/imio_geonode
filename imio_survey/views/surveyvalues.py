# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from imio_survey.models import SurveyLayer
from imio_survey.queriers.factories import SurveyQuerierFactory

import json

class SurveyValuesView(View):
    def get(self, request, *args, **kwargs):
        result = None
        survey_layer_param = request.GET.get("l", None) #SurveyLayer
        survey_attribute_param = request.GET.get("att", None) #SurveyAttributeName
        if survey_layer_param:
            if survey_attribute_param:
                try:
                    survey_layer = SurveyLayer.objects.get(pk = survey_layer_param)
                    querier = SurveyQuerierFactory().createQuerier(survey_layer.gis_server.servertype)
                    if querier.supportFindAttributeValues():
                        find_attributes_result = querier.findAttributeValues(
                            survey_layer.layer_name,
                            survey_attribute_param,
                            survey_layer.gis_server.url,
                            survey_layer.gis_server.username,
                            survey_layer.gis_server.password
                        )
                        if find_attributes_result:
                            result = {
                                'success': True,
                                'message': "Success",
                                'result': find_attributes_result
                            }
                        else:
                            result = {
                                'success': False,
                                'message': "Error : backend query failed",
                                'result': None
                            }
                    else:
                        result = {
                            'success': False,
                            'message': "Error : Server Backend for this layer does not support to query values.",
                            'result': None
                        }
                except ObjectDoesNotExist:
                    result = {
                        'success': False,
                        'message': "Error : Provided layer %s does not exist in database" % (survey_layer_param),
                        'result': None
                    }
            else:
                result = {
                    'success': False,
                    'message': "Error : Parameter att (SurveyAttributeName) is missing",
                    'result': None
                }
        else:
            result = {
                'success': False,
                'message': "Error : Parameter l (SurveyLayer) is missing",
                'result': None
            }

        return HttpResponse(json.dumps(result),content_type="application/json")
