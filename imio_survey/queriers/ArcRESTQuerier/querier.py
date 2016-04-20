from imio_survey.queriers import IQuerier

from arcrest.server import MapService
from arcrest.geometry import Envelope, Polygon, Point, Polyline, Multipoint, fromGeoJson
from django.utils import simplejson

if __name__ == "__main__":
    #url = "http://geoservices.wallonie.be/arcgis/rest/services/NATURA2000/NATURA2000_EP/MapServer"
    url = "http://geoservices.wallonie.be/arcgis/rest/services/EAU/ATLAS_HYDRO__RESEAU/MapServer"
    mapService =  MapService(url)
    #print mapService.layernames
    #print mapService.fullExtent

    searchZone =  Envelope(150000,150000,160000,160000,spatialReference="31370")

    result =  mapService.Identify(searchZone, sr="31370", layers="NATURA2000_EP",tolerance=1, mapExtent="0,0,300000,300000", imageDisplay=1, returnGeometry=True)
    for r in result.results:
        for key in r['attributes']:
            print key , " = ",  r['attributes'][key]

class ArcRESTQuerier(IQuerier):

    def identify(self, geosGeometry, geometryFieldName, layers, url, username="", password=""):
        searchZone = self.geosGeom2EsriGeom(geosGeometry)
        mapService =  MapService(url)
        #TODO build mapextent and imageDisplay and so... results are wrong without correct parameters
        #layers top (default) // visible // all
        layers_param="all"
        if layers is not None:
            layers_param = layers_param + ":" + layers
        result =  mapService.Identify(searchZone, sr="31370", layers=layers_param,tolerance=0, mapExtent="0,0,300000,300000", imageDisplay=1024, returnGeometry=False)
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
