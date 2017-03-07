from imio_survey.queriers import IQuerier

class GeonodeQuerier(IQuerier):
    def getFields(self, layerName, url, username, password):
        pass
    def identify(self, geometry, geometryFieldName, layers, url, username, password):
        pass
    def findAttributeValues(self, layerName, attributeName, url, username, password, area=None):
        pass
    def supportFindAttributeValues(self):
        return False
