from imio_survey.queriers import IQuerier

from arcrest.server import MapService
from arcrest.geometry import Envelope, Polygon, Point, Polyline, Multipoint


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

    def identify(self, geosGeometry, layers, url, username="", password=""):
        searchZone = self.geosGeom2EsriGeom(geosGeometry)
        result =  mapService.Identify(searchZone, sr="31370", layers=layers,tolerance=1, mapExtent="0,0,300000,300000", imageDisplay=1, returnGeometry=True)

    def pointToEsri(self,geom):
        return Point.fromGeoJson(geom)

    def linestringToEsri(self,geom):
        return Polygon.fromGeoJson(geom)

    def linearRingToEsri(self,geom):
        return Polygon.fromGeoJson(geom)

    def polygonToEsri(self,geom):
        return Polygon.fromGeoJson(geom)

    def multiPointToEsri(self,geom):
        return Multipoint.fromGeoJson(geom)

    def multiLineStringToEsri(self,geom):
        raise NotImplementedError("Unimplemented convert from GeoJSON")

    def multiPolygonToEsri(self,geom):
        raise NotImplementedError("Unimplemented convert from GeoJSON")

    def geometryCollectionToEsri(self,geom):
        raise NotImplementedError("Unimplemented convert from GeoJSON")

    def geosGeom2EsriGeom(self,geosGeom):
        geomtype = geosGeom.geom_typeid
        geom_geojson = geosGeom.json

        switcher = {
            0 : self.pointToEsri(geom_geojson),
            1 : self.linestringToEsri(geom_geojson),
            2 : self.linearRingToEsri(geom_geojson),
            3 : self.polygonToEsri(geom_geojson),
            4 : self.multiPointToEsri(geom_geojson),
            5 : self.multiLineStringToEsri(geom_geojson),
            6 : self.multiPolygonToEsri(geom_geojson),
            7 : self.geometryCollectionToEsri(geom_geojson),
        }

        return switcher.get(argument)
