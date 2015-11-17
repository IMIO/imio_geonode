from django.test import TestCase

from imio_survey.models import SurveyGisServer

from imio_survey.queriers.factories import SurveyQuerierFactory
from imio_survey.queriers.ArcRESTQuerier.querier import ArcRESTQuerier
from imio_survey.queriers.GeonodeQuerier.querier import GeonodeQuerier
from imio_survey.queriers.OGCQuerier.querier import OGCQuerier
from imio_survey.queriers import IQuerier


class SurveyTestCase(TestCase):
    def setUp(self):
        pass

    def test_querier_factory(self):
        testOGCQuerier =  SurveyQuerierFactory().createQuerier(SurveyGisServer.OGC)
        testGeonodeQuerier =  SurveyQuerierFactory().createQuerier(SurveyGisServer.GEONODE)
        testArcRESTQuerier =  SurveyQuerierFactory().createQuerier(SurveyGisServer.ARCREST)

        self.assertIsInstance(testOGCQuerier,OGCQuerier)
        self.assertIsInstance(testOGCQuerier,IQuerier)
        self.assertIsInstance(testGeonodeQuerier,GeonodeQuerier)
        self.assertIsInstance(testGeonodeQuerier,IQuerier)
        self.assertIsInstance(testArcRESTQuerier,ArcRESTQuerier)
        self.assertIsInstance(testArcRESTQuerier,IQuerier)
