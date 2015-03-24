
# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand, CommandError

from optparse import OptionParser
from optparse import make_option
from geoserver.catalog import Catalog
from uuid import uuid4
from decimal import *
from django.core.management import call_command
import time

from geonode.layers.models import Layer

class Command(BaseCommand):

    args = 'params'
    help = 'Collect layer from Database'
    geoserver_rest_url = 'http://localhost:8080/geoserver/rest'
    urb = {
            "capa":"Parcelles",
            "toli":"cadastre_ln_toponymiques",
            "canu":"cadastre_pt_num",
            "cabu":"Batiments",
            "gept":"cadastre_points_generaux",
            "gepn":"cadastre_pol_gen",
            "inpt":"point",
            "geli":"cadastre_ln_generales",
            "inli":"cadastre_ln_informations",
            "topt":"point",
            }

    option_list = BaseCommand.option_list + (
    make_option("-p", "--gpw",
        action='store',
        type="string",
        dest='gpw',
        default="",
        help="Geoserver admin password [default: %default]"),
    )+ (
    make_option("-u", "--urbanUrl",
        action='store',
        type="string",
        dest='urbanUrl',
        default="",
        help="Urban URL [default: %default]"),
    )+ (
    make_option("-r", "--ropw",
        action='store',
        type="string",
        dest='ropw',
        default="",
        help="Remote postGIS ro_user password [default: %default]"),
    )+ (
    make_option("-d", "--database",
        action='store',
        type="string",
        dest='database',
        default="urb_xxx",
        help="remote urban database name [default: %default]"),
    )+ (
    make_option("-a", "--alias",
        action='store',
        type="string",
        dest='alias',
        default="",
        help="prefix alias [default: %default]"),
    )+ (
    make_option("-z", "--uri",
        action='store',
        type="string",
        dest='uri',
        default="imio.be",
        help="uri= [default: %default]"),
    )+ (
    make_option("-g", "--postuser",
        action='store',
        type="string",
        dest='postuser',
        default="ro_user",
        help="db_use r= [default: %default]"),
    )+ (
    make_option("-c", "--geoserveradmin",
        action='store',
        type="string",
        dest='geoserveradmin',
        default="admin",
        help="Geoserver admin = [default: %default]"),
    )+ (
    make_option("-n", "--groupname",
        action='store',
        type="string",
        dest='groupname',
        default="",
        help="Group Name for permition = [default: %default]"),
    )

    def createDataStore(self, options):
        try:
            cat = Catalog(self.geoserver_rest_url, options['geoserveradmin'], options['gpw'])
            #create datastore for URB schema
            try:
                ws = cat.create_workspace(options['alias'],options['uri'])
            except Exception as e:
                raise Exception('Le nom du workspace ou l\'alias est déja utiliser')
            try:
                ds = cat.create_datastore(options['alias'], ws)
                ds.connection_parameters.update(
                    host=options['urbanUrl'],
                    port="5432",
                    database=options['database'],
                    user=options['postuser'],
                    passwd=options['ropw'],
                    dbtype="postgis")
                cat.save(ds)
            except Exception as e:
                print(str(e))
                raise Exception('Erreur de connexion au Geoserver lors de la création du DataStore')
        except Exception as e:
            raise Exception(str(e))
        return ws.name , ds.name, ds.resource_type
    
    def addLayersToGeoserver(self, options):
        cat = Catalog(self.geoserver_rest_url, options['geoserveradmin'], options['gpw'])

        ds = cat.get_store(options['alias'])

        layers = []
        try:
            #connect to tables and create layers and correct urban styles
            for table in self.urb:
                try:
                    style = self.urb[table]
                    ft = cat.publish_featuretype(table, ds, 'EPSG:31370', srs='EPSG:31370')
                    ft.default_style = style
                    cat.save(ft)
                    res_name = ft.dirty['name']
                    res_title = options['alias']+"_"+table
                    cat.save(ft)

                    layers.append({ 'res_name' : res_name, 'res_title' : res_title })
                except Exception as e:
                    # a verifier une fois un possesion des styles
                    print(str(e))

        except Exception as e:
            print(str(e))
            raise Exception('Erreur lors de la récupération des couches depuis Geoserver')

        return layers

    def addLayersToGeonode(self, options, ws_name, ds_name, ds_resource_type, layers):
        try:
            for l in layers:
                created = False

                ln = "%s_%s" % (ws_name.encode('utf-8'), l['res_name'].encode('utf-8'))
                print(ln)

                layer, created = Layer.objects.get_or_create(name=str(ln), defaults={
                    "workspace": ws_name,
                    "store":  ds_name,
                    "storeType": ds_resource_type,
                    "typename": "%s:%s" % (ws_name.encode('utf-8'), l['res_name'].encode('utf-8')),
                    "title": l['res_title'] or 'No title provided',
                    "abstract": 'No abstract provided',
                    #"owner": owner,
                    "uuid": str(uuid4())
                    #"bbox_x0": Decimal(ft.latLonBoundingBox.miny),
                    #"bbox_x1": Decimal(ft.latLonBoundingBox.maxy),
                    #"bbox_y0": Decimal(ft.latLonBoundingBox.minx),
                    #"bbox_y1": Decimal(ft.latLonBoundingBox.maxx)       
                })
                print("fin creation")
                if created:
                    print("si crée")
                    grName = unicode(options['groupname'])
                    perm = {
                           u'users': {
                               u'AnonymousUser': [] },
                           u'groups': {
                               grName:[u'view_resourcebase',u'download_resourcebase'] }
                           }
                    layer.set_permissions(perm)
                    layer.save()
                    print("Layer sauver")
                else:
                    print("Layer existe déjà")
        except Exception as e:
            print('Exception found')
            print(str(e))
            raise Exception('Erreur lors de l\'importation des couches depuit Geoserver')

    def handle(self, *args, **options):
        if self.verifParams(options):
            ws_name , ds_name, ds_resource_type =  self.createDataStore(options)
            layers = self.addLayersToGeoserver(options)
            self.addLayersToGeonode(options,ws_name, ds_name,ds_resource_type, layers)
        else:
            raise Exception('Des paramètres non pas été définit')

    def verifParams(self, options):
        if(options['gpw'] is None or options['gpw'] is '' or
           options['urbanUrl'] is None or options['urbanUrl'] is '' or
           options['ropw'] is None or options['ropw'] is '' or
           options['alias'] is None or options['alias'] is '' or
           options['groupname'] is None or options['groupname'] is ''):
            print('Some parameter was not define')
            return False
        else:
            return True
