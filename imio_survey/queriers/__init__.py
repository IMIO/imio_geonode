import abc

class IQuerier(object):
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def identify(self, geometry, geometryFieldName, layers, url, username, password):
        """Method that query spacialy a given and return a list of intersected entities"""

    @abc.abstractmethod
    def findAttributeValues(self, layerName, attributeName, url, username, password):
        """Method that harvest all distinct values for a given layer"""

    @abc.abstractmethod
    def supportFindAttributeValues(self):
        """Method that return if the querier support findAttributeValues"""
