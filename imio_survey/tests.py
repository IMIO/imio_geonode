
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Polygon
from django.conf import settings
from django.test import Client, TestCase

from imio_survey.models import SurveyGisServer
from imio_survey.tasks import mul, doSurvey

from imio_survey.queriers.factories import SurveyQuerierFactory
from imio_survey.queriers.ArcRESTQuerier.querier import ArcRESTQuerier
from imio_survey.queriers.GeonodeQuerier.querier import GeonodeQuerier
from imio_survey.queriers.OGCQuerier.querier import OGCQuerier_110
from imio_survey.queriers.OGCQuerier.utils import to_gml3
from imio_survey.queriers import IQuerier

import json

class SurveyTestCase(TestCase):
    fixtures = ['imio_survey_testdata.json']

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
        result = doSurvey("TEST", poly.wkt)
        self.assertIsNotNone(result)
        self.inspectQueryResult(result)

    def test_OGCFeatureIntersectQuery(self):
        result = self.testOGCQuerier._buildWfsIntersectRequest(self.liegePolygon.ogr.gml, "liege:capa", "the_geom")
        self.assertIsNotNone(result)

    def test_WFSQuery(self):
        result = self.testOGCQuerier.identify(self.liegePolygon,"the_geom", "liege:capa", "https://geonode.imio.be/geoserver/wfs", settings.SURVEY_TEST_USERNAME, settings.SURVEY_TEST_PASSWD)
        self.assertIsNotNone(result)
        self.assertEqual(len(result),1)
        self.assertEqual(len(result[0].keys()),11)
        self.assertEqual(result[0]['capakey'],'62817B0482/05A000')

    def test_exportgml3(self):
        result_gml3 = to_gml3(self.liegePolygon.ogr)
        result_gml2 = self.liegePolygon.ogr.gml
        self.assertIsNotNone(result_gml3)
        self.assertNotEqual(result_gml2,result_gml3)

    def test_MultiPolygon(self):
        result = doSurvey("TEST", self.multiPolygonWKT)
        self.assertIsNotNone(result)
        self.inspectQueryResult(result)

    def test_post_survey(self):
        poly = Polygon( ((121900, 125800), (121900, 125810), (121905, 125810), (121905, 125800), (121900, 125800)) )
        c =  Client()
        response = c.post('/survey/', {'st': "TEST", 'geom': poly.wkt})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.inspectQueryResult(json.loads(response.content))

    def test_liege_wfs(self):
        result = self.testOGCQuerier.identify(self.liegePolygon, "lxgeom", "starapic:PERMISSECTEURS", "http://e-services.liege.be:8100/ElyxRouter/rest/wfs/WFS","","")
        print(result)
        self.assertIsNotNone(result)

    def inspectQueryResult(self, result):
        for res in result:
            self.assertEqual(res['success'], True)
            self.assertEqual(res['message'], None)
