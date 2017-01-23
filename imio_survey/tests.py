
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Polygon
from django.conf import settings
from django.test import Client, TestCase
from django.core.exceptions import ObjectDoesNotExist

from imio_survey.models import SurveyGisServer, SurveyLayer
from imio_survey.tasks import mul, doSurvey

from imio_survey.queriers.factories import SurveyQuerierFactory
from imio_survey.queriers.ArcRESTQuerier.querier import ArcRESTQuerier
from imio_survey.queriers.GeonodeQuerier.querier import GeonodeQuerier
from imio_survey.queriers.OGCQuerier.querier import OGCQuerier_110
from imio_survey.queriers.OGCQuerier.utils import to_gml3
from imio_survey.queriers import IQuerier

import json

class SurveyTestCase(TestCase):
    fixtures = ['export_conf.json']
    #fixtures = ['imio_survey_testdata.json']

    def setUp(self):
        self.testOGCQuerier     =  SurveyQuerierFactory().createQuerier(SurveyGisServer.OGC)
        self.testGeonodeQuerier =  SurveyQuerierFactory().createQuerier(SurveyGisServer.GEONODE)
        self.testArcRESTQuerier =  SurveyQuerierFactory().createQuerier(SurveyGisServer.ARCREST)
        self.liegePolygon = Polygon( ((235745, 147615), (235745, 147616), (235746, 147616), (235746, 147615), (235745, 147615)) )
        self.multiPolygonWKT = "MULTIPOLYGON(((235424.935 148687.065,235429.244 148689.993,235429.943 148689.086,235433.273 148691.635,235438.99 148684.223,235443.735 148678.077,235445.516 148679.44,235454.802 148668.44,235453.069 148665.975,235448.739 148659.82,235433.586 148682.192,235429.837 148679.679,235426.711 148684.39,235424.935 148687.065)),((241020.367 152036.194,241024.691 152041.929,241036.183 152032.719,241031.701 152026.956,241020.367 152036.194)))"
        settings.CELERY_ALWAYS_EAGER = True

    def test_querier_factory(self):
        self.assertIsInstance(self.testOGCQuerier,OGCQuerier_110)
        self.assertIsInstance(self.testOGCQuerier,IQuerier)
        self.assertIsInstance(self.testGeonodeQuerier,GeonodeQuerier)
        self.assertIsInstance(self.testGeonodeQuerier,IQuerier)
        self.assertIsInstance(self.testArcRESTQuerier,ArcRESTQuerier)
        self.assertIsInstance(self.testArcRESTQuerier,IQuerier)

    def test_ArcRestQuerier(self):
        url ="http://geoservices.wallonie.be/arcgis/rest/services/NATURA2000/NATURA2000_EP/MapServer"
        poly = Polygon( ((121900, 125800), (121900, 125810), (121905, 125810), (121905, 125800), (121900, 125800)) )
        result = self.testArcRESTQuerier.identify( poly,None, "NATURA2000_EP", url)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)

    def test_query_layer(self):
        poly = Polygon( ((121900, 125800), (121900, 125810), (121905, 125810), (121905, 125800), (121900, 125800)) )
        self.assertTrue(True)

    def test_celcery(self):
        result = mul.delay(2,2)
        self.assertEqual(result.get(timeout=5),4)

    def test_survey(self):
        poly = Polygon( ((121900, 125800), (121900, 125810), (121905, 125810), (121905, 125800), (121900, 125800)) )
        result = doSurvey("TESTWFS", poly.wkt)
        self.assertIsNotNone(result)
        self.inspectQueryResult(result)

    def test_OGCFeatureIntersectQuery(self):
        result = self.testOGCQuerier._buildWfsIntersectRequest(self.liegePolygon.ogr.gml, "liege:capa", "the_geom")
        self.assertIsNotNone(result)

    def test_WFSQuery(self):
        result = self.testOGCQuerier.identify(self.liegePolygon,"the_geom", "liege:capa", "https://geonode.imio.be/geoserver/wfs", settings.SURVEY_TEST_USERNAME, settings.SURVEY_TEST_PASSWD)
        self.assertIsNotNone(result)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0]['attributes'].keys()),11)
        self.assertEqual(result[0]['attributes']['capakey'],'62817B0482/05A000')

    def test_exportgml3(self):
        result_gml3 = to_gml3(self.liegePolygon.ogr)
        result_gml2 = self.liegePolygon.ogr.gml
        self.assertIsNotNone(result_gml3)
        self.assertNotEqual(result_gml2,result_gml3)

    def test_MultiPolygon(self):
        result = doSurvey("TESTWFS", self.multiPolygonWKT)
        self.assertIsNotNone(result)
        self.inspectQueryResult(result)

    def test_post_survey(self):
        poly = Polygon( ((121900, 125800), (121900, 125810), (121905, 125810), (121905, 125800), (121900, 125800)) )
        c =  Client()
        response = c.post('/survey/', {'st': "TESTWFS", 'geom': poly.wkt})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.inspectQueryResult(json.loads(response.content))

    def test_post_survey_dgo4(self):
        poly = "MULTIPOLYGON(((236796.699 147622.858,236799.736 147628.339,236895.459 147707.807,236908.52 147718.682,236952.094 147754.965,236994.014 147790.595,237037.549 147827.146,237059.573 147845.848,237079.823 147854.571,237086.229 147854.629,237068.986 147789.157,237040.115 147680.114,237051.359 147654.212,236946.316 147650.789,236946.301 147651.031,236931.005 147650.522,236931.013 147650.29,236927.953 147650.19,236916.039 147624.026,236912.419 147616.073,236906.014 147602.015,236899.546 147588.619,236898.519 147586.396,236880.545 147594.902,236878.991 147591.843,236877.982 147589.264,236876.36 147584.515,236875.021 147579.997,236874.102 147576.018,236873.387 147571.84,236873.044 147568.44,236872.967 147565.184,236873.149 147560.341,236873.307 147556.97,236873.451 147555.043,236873.938 147551.571,236875.066 147545.864,236879.109 147544.017,236876.776 147538.91,236882.788 147532.94,236894.823 147520.146,236897.311 147517.501,236898.236 147516.517,236897.587 147515.737,236903.154 147509.879,236970.005 147490.102,237058.978 147548.917,237077.582 147481.999,237065.861 147450.96,237057.968 147424.33,237052.982 147407.526,237052.443 147405.246,237052.693 147401.148,237054.862 147396.599,237061.24 147388.372,237063.39 147385.573,237068.158 147379.364,237071.037 147375.636,237068.09 147374.332,237049.214 147363.686,237039.672 147355.581,237036.067 147353.381,237015.005 147340.561,237001.043 147340.075,236999.004 147342.627,236995.403 147352.036,236971.51 147358.486,236959.184 147362.147,236937.941 147368.283,236918.383 147374.058,236897.057 147380.331,236900.912 147393.506,236906.803 147413.641,236929.172 147490.088,236900.022 147499.366,236899.657 147499.518,236898.688 147500.179,236897.773 147500.855,236897.498 147501.119,236890.632 147508.396,236891.625 147510.271,236888.793 147512.458,236870.701 147535.429,236861.586 147559.045,236863.894 147561.865,236863.49 147564.376,236862.929 147566.857,236862.285 147569.312,236861.635 147571.76,236859.21 147579.938,236857.478 147587.622,236855.535 147596.077,236851.197 147595.072,236844.652 147594.699,236842.394 147596.228,236832.831 147598.315,236828.578 147599.244,236825.458 147600.115,236821.864 147601.194,236818.475 147602.291,236815.191 147603.411,236811.583 147604.724,236807.949 147606.244,236808.161 147606.697,236800.269 147611.139,236801.963 147614.429,236802.341 147614.822,236803.72 147616.245,236796.699 147622.858),(236862.061 147628.486,236860.864 147628.238,236864.488 147619.806,236864.982 147619.095,236865.582 147618.325,236866.218 147617.602,236866.875 147616.952,236867.571 147616.354,236868.228 147615.86,236868.789 147615.477,236869.421 147615.089,236870.189 147614.665,236871.204 147614.145,236872.206 147613.671,236881.922 147609.189,236882.674 147609.335,236883.143 147609.522,236883.747 147609.824,236884.289 147610.172,236884.736 147610.541,236885.014 147610.82,236885.628 147612.13,236887.154 147616.747,236881.912 147625.853,236882.786 147629.85,236882.489 147632.786,236879.906 147634.778,236877.968 147635.121,236874.481 147633.614,236871.829 147630.514,236862.061 147628.486)))"
        c =  Client()
        response = c.post('/survey/', {'st': "TESTWFS", 'geom': poly})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.inspectQueryResult(json.loads(response.content))

#    def test_liege_wfs(self):
#        result = self.testOGCQuerier.identify(self.liegePolygon, "lxgeom", "starapic:PERMISSECTEURS", "http://e-services.liege.be:8100/ElyxRouter/rest/wfs/WFS","","")
#        self.assertIsNotNone(result)

    def test_simple_attribute_query(self):
        c = Client()
        response = c.get('/survey/survey_value_list', {'l': "3", 'att': "AFFECT"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        result = json.loads(response.content)
        self.assertEqual(result['success'],True)
        #"{u'message': u'Success', u'result': {u'fieldInfo': {u'alias': u'AFFECT', u'length': 3, u'type': u'esriFieldTypeString', u'name': u'AFFECT'}, u'displayFieldName': u'DESCRIPTION', u'features': [u'R03', u'X01', u'V01', u'A11', u'L01', u'R02', u'P11', u'R05', u'P01', u'L11', u'D02', u'P02', u'V02', u'D01', u'A12', u'P12', u'R04', u'A02', u'H02', u'R01', u'E01', u'H01', u'E02', u'L12', u'L13', u'A01']}, u'success': True}"

    def test_badparameter_attribute_query(self):
        c = Client()
        response = c.get('/survey/survey_value_list', {'l': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        result = json.loads(response.content)
        self.assertEqual(result['success'],False)

    def test_badparameter_attribute_query2(self):
        c = Client()
        response = c.get('/survey/survey_value_list', {'l': "99999999"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        result = json.loads(response.content)
        self.assertEqual(result['success'],False)

    def test_survey_type_layer_list(self):
        c = Client()
        response = c.get('/survey/survey_type_layers', {'st': "TESTWFS"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        result = json.loads(response.content)
        self.assertEqual(len(result),4)
        for layer in result:
            layer_pk = layer["l"] #id
            try:
                layer = SurveyLayer.objects.get(pk = layer_pk)
                self.assertEqual(layer_pk, layer.id)
            except ObjectDoesNotExist:
                self.fail('Layer with pk %s does not exist' % (layer_pk))

    def test_simple_badattribute_query(self):
        c = Client()
        response = c.get('/survey/survey_value_list', {'l': "3", 'att': "AFT"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        result = json.loads(response.content)
        self.assertEqual(result['success'],False)

    def test_layer_fields_affect(self):
        c = Client()
        response = c.get('/survey/survey_layer_fields', {'l': "3"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

    def inspectQueryResult(self, result):
        for res in result:
            self.assertEqual(res['success'], True, res['message'])
            self.assertEqual(res['message'], None)
