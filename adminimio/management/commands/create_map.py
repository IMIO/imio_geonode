# -*- coding: utf8 -*-
from optparse import OptionParser
from optparse import make_option
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from geonode.maps.models import Map, MapLayer
from geonode.layers.models import Layer
from geonode.utils import default_map_config
from geonode.base.models import Link

class Command(BaseCommand):

    args = 'params'
    help = 'Create Map from geoserver workspace'
    option_list = BaseCommand.option_list + (
    make_option("-u", "--username",
        action='store',
        type="string",
        dest='username',
        default="admin",
        help="Nom utilisateur communal"),
    )+ (
    make_option("-w", "--workspace_name",
        action='store',
        type="string",
        dest='workspace',
        default="",
        help="Workspace name"),
    )+ (
    make_option("-m", "--map",
        action='store',
        type="int",
        dest='map',
        default="1",
        help="Map id"),
    )

    def create_from_layer_list(self, new_map, user, layers, title, abstract):
        new_map.uuid = str(uuid.uuid1())
        new_map.owner = user
        new_map.title = title
        new_map.abstract = abstract
        new_map.projection = getattr(settings, 'DEFAULT_MAP_CRS', 'EPSG:900913')
        new_map.zoom = 0
        new_map.center_x = 0
        new_map.center_y = 0
        bbox = None
        index = 0

        DEFAULT_MAP_CONFIG, DEFAULT_BASE_LAYERS = default_map_config()

        # Save the map in order to create an id in the database
        # used below for the maplayers.
        new_map.save()

        for layer in layers:
            if not isinstance(layer, Layer):
                try:
                    layer = Layer.objects.get(typename=layer)
                    print(layer)
                except ObjectDoesNotExist:
                    raise Exception(
                        'Could not find layer with name %s' %
                        layer)

            if not user.has_perm(
                    'base.view_resourcebase',
                    obj=layer.resourcebase_ptr):
                # invisible layer, skip inclusion or raise Exception?
                raise Exception(
                    'User %s tried to create a map with layer %s without having premissions' %
                    (user, layer))


            ows_link_url = None
            try:
                ows_link = layer.link_set.get(link_type='OGC:WMS')
                ows_link_url = ows_link.url
            except Link.DoesNotExist:
                pass
            layer_cfg = """{"selected": true, "title": "brainelechateau_cabu", "cached": true, "capability": {"abstract": "No abstract provided", "nestedLayers": [], "cascaded": 0, "fixedHeight": 0, "prefix": "cabu", "keywords": ["features", "cabu"], "noSubsets": false, "dimensions": {}, "opaque": false, "infoFormats": ["text/plain", "application/vnd.ogc.gml", "text/xml", "application/vnd.ogc.gml/3.1.1", "text/xml; subtype=gml/3.1.1", "text/html", "application/json"], "styles": [{"abstract": "A sample style that just prints out a transparent red interior with a red outline", "legend": {"href": "http://brainelechateau-geonode.imio-app.be:80/geoserver/brainelechateau/wms?request=GetLegendGraphic&format=image%2Fpng&width=20&height=20&layer=cabu", "width": "20", "format": "image/png", "height": "20"}, "name": "polygon", "title": "A boring default style"}], "attribution": {"title": "admin"}, "authorityURLs": {}, "bbox": {"EPSG:31370": {"srs": "EPSG:31370", "bbox": [140784.65625, 149937.875, 147527.25, 154404.359375]}}, "fixedWidth": 0, "metadataURLs": [{"href": "https://brainelechateau-geonode.imio-app.be/catalogue/csw?outputschema=http%3A%2F%2Fwww.opengis.net%2Fcat%2Fcsw%2Fcsdgm&service=CSW&request=GetRecordById&version=2.0.2&elementsetname=full&id=4c048bf4-2b0d-45a1-a643-e08b9a5aa6f8", "type": "FGDC", "format": "text/xml"}], "name": "cabu", "identifiers": {}, "srs": {"EPSG:900913": true}, "formats": ["image/png", "application/atom xml", "application/atom+xml", "application/openlayers", "application/pdf", "application/rss xml", "application/rss+xml", "application/vnd.google-earth.kml", "application/vnd.google-earth.kml xml", "application/vnd.google-earth.kml+xml", "application/vnd.google-earth.kml+xml;mode=networklink", "application/vnd.google-earth.kmz", "application/vnd.google-earth.kmz xml", "application/vnd.google-earth.kmz+xml", "application/vnd.google-earth.kmz;mode=networklink", "atom", "image/geotiff", "image/geotiff8", "image/gif", "image/gif;subtype=animated", "image/jpeg", "image/png8", "image/png; mode=8bit", "image/svg", "image/svg xml", "image/svg+xml", "image/tiff", "image/tiff8", "kml", "kmz", "openlayers", "rss", "text/html; subtype=openlayers"], "title": "brainelechateau_cabu", "queryable": true, "llbbox": [4.237258724748909, 50.65973330186791, 4.332730242848743, 50.69995344778437]}, "tiled": true}"""
            
            MapLayer.objects.create(
                map=new_map,
                name=layer.typename,
                ows_url=ows_link_url,
                stack_order=index,
                visibility=True,
                format="image/png",
                layer_params=json.dumps(layer_cfg),
                source_params=json.dumps(source_cfg)
            )

            index += 1

        # Set bounding box based on all layers extents.
        bbox = new_map.get_bbox_from_layers(new_map.local_layers)

        new_map.set_bounds_from_bbox(bbox)

        new_map.set_missing_info()

        # Save again to persist the zoom and bbox changes and
        # to generate the thumbnail.
        new_map.save()

    def create_map_withlayers(self, user_name, ws_name, map_id):
        """
        Create Map
        """
        if Map.objects.filter(pk=map_id).exists():
            print('A map with id %s already exist. Choose another id' % map_id)
            return

        User = get_user_model()
        map_owner = User.objects.get(username=user_name)
        layers = Layer.objects.filter(workspace=ws_name).all()
        new_map = Map()

        self.create_from_layer_list(
            new_map,
            map_owner,
            layers,
            "UrbanMap",
            "Urban Map. Be carefull"
        )

    def handle(self, *args, **options):
        self.create_map_withlayers(
            options['username'],
            options['workspace'],
            options['map']
        )
