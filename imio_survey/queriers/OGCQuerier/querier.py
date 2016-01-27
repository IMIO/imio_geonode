from imio_survey.queriers import IQuerier
import requests
from xml.etree.ElementTree import XML
import xml.etree.ElementTree as ET

class OGCQuerier(IQuerier):
    WFS_GET_FEATURE = 'GetFeature'

    def _buildWfsIntersectRequest(self, gmlString, typeName, geometryFieldName):
        getfeatureTemplate = """<wfs:GetFeature service="WFS" version="1.0.0" xmlns:wfs="http://www.opengis.net/wfs" xmlns="http://www.opengis.net/ogc"
                            xmlns:gml="http://www.opengis.net/gml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                            xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-basic.xsd">
                                <wfs:Query typeName="%s">
                                    <Filter>
                                        <Intersects>
                                            <PropertyName>%s</PropertyName>
                                            %s
                                        </Intersects>
                                    </Filter>
                                </wfs:Query>
                            </wfs:GetFeature>""" % (typeName, geometryFieldName, gmlString)
        return getfeatureTemplate

    def identify(self, geosGeometry, geometryFieldName, layers, url, username, password):
        """
            Assuming url like http://localhost:8080/geoserver/wfs
        """
        #Assuming Lambert72
        #Typename like geonode:capa
        gmlString = geosGeometry.ogr.gml
        payload = self._buildWfsIntersectRequest(gmlString, layers, geometryFieldName)
        r = requests.post(url, data = payload, auth=(username, password), verify=False)
        tree = XML(r.text)
        if tree.tag == "{http://www.opengis.net/ogc}ServiceExceptionReport":
            se = tree.find('{http://www.opengis.net/ogc}ServiceException')
            raise Exception(str(se.text).strip())
        else:
            print(ET.tostring(tree))
            return str(tree)
