from imio_survey.queriers import IQuerier
import requests
from xml.etree.ElementTree import XML
import xml.etree.ElementTree as ET

class OGCQuerier(IQuerier):
    WFS_GET_FEATURE = 'GetFeature'

    """
    Sample WFS 1.0.0 (basic) Response
    <ns0:FeatureCollection xmlns:ns0="http://www.opengis.net/wfs" xmlns:ns2="http://www.opengis.net/gml" xmlns:ns3="liege.be" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="liege.be https://geonode.imio.be/geoserver/wfs?service=WFS&amp;version=1.0.0&amp;request=DescribeFeatureType&amp;typeName=liege%3Acapa
     http://www.opengis.net/wfs https://geonode.imio.be/geoserver/schemas/wfs/1.0.0/WFS-basic.xsd">
     <ns2:boundedBy><ns2:null>unknown</ns2:null></ns2:boundedBy>
     <ns2:featureMember>
        <ns3:capa fid="capa.65687">
            <ns3:capakey>62817B0482/05A000</ns3:capakey>
            <ns3:capaty>PR</ns3:capaty>
            <ns3:shape_area>942.7562</ns3:shape_area>
            <ns3:sheet>62817B020000_2013O</ns3:sheet>
            <ns3:the_geom>
                <ns2:MultiPolygon srsName="http://www.opengis.net/gml/srs/epsg.xml#31370">
                    <ns2:polygonMember>
                        <ns2:Polygon>
                            <ns2:outerBoundaryIs>
                                <ns2:LinearRing>
                                    <ns2:coordinates cs="," decimal="." ts=" ">
                                    235735.648,147611.28 235735.732,147612.904 235735.915,147614.522 235736.231,147617.387
                                    ... (coordinates)</ns2:coordinates>
                                </ns2:LinearRing>
                            </ns2:outerBoundaryIs>
                        </ns2:Polygon>
                    </ns2:polygonMember>
                </ns2:MultiPolygon>
            </ns3:the_geom>
            <ns3:da>62817</ns3:da><ns3:section>B</ns3:section><ns3:radical>482</ns3:radical><ns3:exposant>A</ns3:exposant><ns3:bis>5</ns3:bis><ns3:puissance>0</ns3:puissance></ns3:capa>
        </ns2:featureMember>
    </ns0:FeatureCollection>
    """
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
            Assuming :
            Url like http://localhost:8080/geoserver/wfs
            layers like geonode:capa
            geosGeometry is in Lambert72
        """
        #TODO input checking
        gmlString = geosGeometry.ogr.gml
        payload = self._buildWfsIntersectRequest(gmlString, layers, geometryFieldName)
        #Verify False to avoid certificate not trusted problems
        r = requests.post(url, data = payload, auth=(username, password), verify=False)
        tree = XML(r.text)
        if tree.tag == "{http://www.opengis.net/ogc}ServiceExceptionReport":
            #We Got OGC Error. Find the root cause and throw a proper Exception
            se = tree.find('{http://www.opengis.net/ogc}ServiceException')
            raise Exception(str(se.text).strip())
        else:
            clean_results = []
            features = tree.findall('{http://www.opengis.net/gml}featureMember')
            for feature in features:
                attributes = {}
                for child in feature:
                    for child_elem in child:
                        tag_name = child_elem.tag.split('}')[-1] #Get rid of namespace
                        if child_elem.text is not None:
                            attributes[tag_name] = child_elem.text
                        else:
                            attributes[tag_name] = ""
                clean_results.append(attributes)
            return clean_results
