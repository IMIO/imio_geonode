from django.test import TestCase

from imio_survey.models import SurveyGisServer

from imio_survey.tasks import mul, doSurvey

from imio_survey.queriers.factories import SurveyQuerierFactory
from imio_survey.queriers.ArcRESTQuerier.querier import ArcRESTQuerier
from imio_survey.queriers.GeonodeQuerier.querier import GeonodeQuerier
from imio_survey.queriers.OGCQuerier.querier import OGCQuerier
from imio_survey.queriers import IQuerier

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Polygon
from django.conf import settings

class SurveyTestCase(TestCase):
    fixtures = ['imio_survey_testdata.json']

    def setUp(self):
        self.testOGCQuerier     =  SurveyQuerierFactory().createQuerier(SurveyGisServer.OGC)
        self.testGeonodeQuerier =  SurveyQuerierFactory().createQuerier(SurveyGisServer.GEONODE)
        self.testArcRESTQuerier =  SurveyQuerierFactory().createQuerier(SurveyGisServer.ARCREST)
        self.liegePolygon = Polygon( ((235745, 147615), (235745, 147616), (235746, 147616), (235746, 147615), (235745, 147615)) )
        settings.CELERY_ALWAYS_EAGER = True

    def test_querier_factory(self):
        self.assertIsInstance(self.testOGCQuerier,OGCQuerier)
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

    def test_OGCFeatureIntersectQuery(self):
        result = self.testOGCQuerier._buildWfsIntersectRequest(self.liegePolygon.ogr.gml, "liege:capa", "the_geom")
        self.assertIsNotNone(result)
    def test_WFSQuery(self):
        result = self.testOGCQuerier.identify(self.liegePolygon,"the_geom", "liege:capa", "https://geonode.imio.be/geoserver/wfs", settings.SURVEY_TEST_USERNAME, settings.SURVET_TEST_PASSWD)
        print(result)
        self.assertIsNotNone(result)
