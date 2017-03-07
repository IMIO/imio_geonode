# -*- coding: utf-8 -*-
import abc

class IQuerier(object):
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def identify(self, geometry, geometryFieldName, layers, url, username, password):
        """Method that query spacialy a given and return a list of intersected entities"""

    @abc.abstractmethod
    def findAttributeValues(self, layerName, attributeName, url, username, password, area=None):
        """Method that harvest all distinct values for a given layer"""

    @abc.abstractmethod
    def supportFindAttributeValues(self):
        """Method that return if the querier support findAttributeValues"""

    @abc.abstractmethod
    def getFields(self, layerName, url, username, password):
        """Method that return the list of fields for a specified layer"""
