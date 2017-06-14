# -*- coding: utf8 -*-
from optparse import OptionParser
from optparse import make_option

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
            print(ows_link_url)
            MapLayer.objects.create(
                map=new_map,
                name=layer.typename,
                ows_url=ows_link_url,
                stack_order=index,
                visibility=True
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
