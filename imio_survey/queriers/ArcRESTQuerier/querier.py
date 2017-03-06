# -*- coding: utf-8 -*-
from imio_survey.queriers import IQuerier

from arcrest.server import MapService
from arcrest.geometry import Envelope, Polygon, Point, Polyline, Multipoint, fromGeoJson
from django.utils import simplejson
import requests
from requests.exceptions import ConnectionError

class ArcRESTQuerier(IQuerier):

    def getFields(self, layerName, url, username, password):
        #http://geoservices.wallonie.be/arcgis/rest/services/AMENAGEMENT_TERRITOIRE/PDS_5000/MapServer/19?f=json
        response = None
        payload = {
            'f': 'json'
        }
        layer_url = url + '/' + layerName
        try:
            request_object = requests.get(layer_url, params=payload)
            json_response = request_object.json()
            if json_response and json_response.get('error') is None:
                return json_response['fields']
            else:
                response = None #TODO Give more Informations about why
        except ConnectionError:
            response = None #TODO Give more Informations about why

        return response

    def findAttributeValues(self, layerName, attributeName, url, username, password):
        #http://geoservices.wallonie.be/arcgis/rest/services/AMENAGEMENT_TERRITOIRE/PDS_5000/MapServer/19/query?where=1%3D1&outFields=AFFECT&returnGeometry=false&returnIdsOnly=false&returnCountOnly=false&returnZ=false&returnM=false&returnDistinctValues=true&f=pjson

        payload = {
            'where': '1=1',
            'outFields': attributeName,
            'returnGeometry': 'false',
            'returnIdsOnly': 'false',
            'returnCountOnly': 'false',
            'returnZ': 'false',
            'returnM': 'false',
            'returnDistinctValues': 'true',
            'f': 'json'
        }
        layer_url = url + '/' + layerName + '/query'
        try:
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            request_object = requests.get(layer_url, params=payload, headers=headers)
            json_response = simplejson.loads(request_object.content, encoding="utf-8")

            if json_response and json_response.get('error') is None:
                response = {
                    'displayFieldName': json_response['displayFieldName'],
                    'fieldInfo': json_response['fields'], #We can assume only one field is passed to outFields
                    'features': [feat['attributes'] for feat in json_response['features']]
                }
            else:
                #{u'error': {u'message': u'Failed to execute query.', u'code': 400, u'details': []}})
                response = None #TODO Give more Informations about why
        except ConnectionError:
            response = None #TODO Give more Informations about why

        return response

    def supportFindAttributeValues(self):
        return True

    def identify(self, geosGeometry, geometryFieldName, layers, url, username="", password=""):
        searchZone = self.geosGeom2EsriGeom(geosGeometry)
        mapService = MapService(url)

        #TODO build mapextent and imageDisplay and so... results are wrong without correct parameters
        #layers top (default) // visible // all
        layers_param="all"
        if layers is not None:
            layers_param = layers_param + ":" + layers
        result =  mapService.Identify(searchZone, sr="31370", layers=layers_param,tolerance=0, mapExtent="0,0,300000,300000", imageDisplay="1024,1024,96", returnGeometry=False)
        clean_results = []
        if result:
            for feat in result.results.features:
                feat.pop('geometry')
                clean_results.append(feat)
            return clean_results
        else:
            return None

    def pointToEsri(self,geom):
        return Point(geom)

    def linestringToEsri(self,geom):
        return Polygon(geom)

    def linearRingToEsri(self,geom):
        return Polygon(geom)

    def polygonToEsri(self,geom):
        return Polygon(geom)

    def multiPointToEsri(self,geom):
        return Multipoint(geom)

    def multiLineStringToEsri(self,geom):
        raise NotImplementedError("Unimplemented convert from GeoJSON")

    def multiPolygonToEsri(self,geom):
        """
        ESRI Json geometry handle  multipolygon as one polygon with one ring
        for each polygon inside multipolygon
        """
        multiPolygonJson = geom.json #TODO Maybe using gejson is not needed
        struct = simplejson.loads(multiPolygonJson)
        rings=[]
        for polygonRings in struct['coordinates']:
            for path in polygonRings:
                rings.append(path)

        return Polygon(rings)

    def geometryCollectionToEsri(self,geom):
        raise NotImplementedError("Unimplemented convert from GeoJSON")

    def geosGeom2EsriGeom(self,geosGeom):
        geomtype = geosGeom.geom_typeid

        switcher = {
            0 : self.pointToEsri,
            1 : self.linestringToEsri,
            2 : self.linearRingToEsri,
            3 : self.polygonToEsri,
            4 : self.multiPointToEsri,
            5 : self.multiLineStringToEsri,
            6 : self.multiPolygonToEsri,
            7 : self.geometryCollectionToEsri,
        }

        return switcher.get(geomtype)(geosGeom)
