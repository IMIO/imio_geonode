# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from optparse import OptionParser
from optparse import make_option

from django.contrib.auth import get_user_model
from geonode.maps.models import Map
from geonode.layers.models import Layer

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
        new_map.create_from_layer_list(
            map_owner,
            layers,
            "UrbanMap",
            "Urban Map. Be carefull"
        )
        new_map.save()

    def handle(self, *args, **options):
        self.create_map_withlayers(
            options['username'],
            options['workspace'],
            options['map']
        )
