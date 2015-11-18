from imio_survey.models import SurveyGisServer
from imio_survey.queriers.ArcRESTQuerier.querier import ArcRESTQuerier
from imio_survey.queriers.GeonodeQuerier.querier import GeonodeQuerier
from imio_survey.queriers.OGCQuerier.querier import OGCQuerier


gisServerTypesMapping = {SurveyGisServer.OGC : OGCQuerier,
                         SurveyGisServer.ARCREST: ArcRESTQuerier,
                         SurveyGisServer.GEONODE : GeonodeQuerier}

class SurveyQuerierFactory:
    def createQuerier(self, gisServerType):
        return gisServerTypesMapping.get(gisServerType)()
