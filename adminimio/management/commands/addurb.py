# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand, CommandError

from optparse import OptionParser
from optparse import make_option
from geoserver.catalog import Catalog
from uuid import uuid4
from decimal import *
from django.core.management import call_command
import time
import psycopg2

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
    make_option("-c", "--geoserveradmin",
        action='store',
        type="string",
        dest='geoserveradmin',
        default="admin",
        help="Nom utilisateur Geoserver = [default: %default]"),
    )+ (
    make_option("-p", "--gpw",
        action='store',
        type="string",
        dest='gpw',
        default="",
        help="Geoserver password [default: %default]"),
    )+ (
    make_option("-u", "--urbanUrl",
        action='store',
        type="string",
        dest='urbanUrl',
        default="",
        help="Adresse base de données [default: %default]"),
    )+ (
    make_option("-m", "--dbport",
        action='store',
        type="string",
        dest='dbport',
        default="5432",
        help="Port base de données = [default: %default]"),
    )+ (
    make_option("-g", "--postuser",
        action='store',
        type="string",
        dest='postuser',
        default="ro_user",
        help="Utilisateur base de données = [default: %default]"),
    )+ (
    make_option("-r", "--ropw",
        action='store',
        type="string",
        dest='ropw',
        default="",
        help="Password base de données [default: %default]"),
    )+ (
    make_option("-d", "--database",
        action='store',
        type="string",
        dest='database',
        default="urbangis",
        help="Nom base de données = [default: %default]"),
    )+ (
    make_option("-a", "--alias",
        action='store',
        type="string",
        dest='alias',
        default="",
        help="Workspace [default: %default]"),
    )+ (
    make_option("-z", "--uri",
        action='store',
        type="string",
        dest='uri',
        default="imio.be",
        help="Uri espace de nommage = [default: %default]"),
    )+ (
    make_option("-n", "--groupname",
        action='store',
        type="string",
        dest='groupname',
        default="",
        help="Groupe qui pourra voir les couches [default: %default]"),
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
                    port=options['dbport'],
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

        try:
            ds = cat.get_store(options['alias'])
        except Exception as e:
            raise Exception('Erreur de récupération du workspace')

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
                layer, created = Layer.objects.get_or_create(typename=ws_name + ':' + l['res_name'], defaults={
                    "name" : l['res_name'],
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
    
                if created:
                    grName = unicode(options['groupname'])
                    perm = {
                           u'users': {
                               u'AnonymousUser': [] },
                           u'groups': {
                               grName:[u'view_resourcebase',u'download_resourcebase'] }
                           }
                    try:
                        layer.set_permissions(perm)
                        layer.save()
                    except:
                        raise Exception('Problème survenu lors de l\'application des permissions aux couches')
                else:
                    raise Exception('Erreur lors de l\'importation. Le layer'+ws_name + ':' + l['res_name']+'existe déjà')

        except Exception as e:
            print(str(e))
            raise Exception('Erreur lors de l\'importation des couches depuis Geoserver',e)

    def handle(self, *args, **options):
        if self.verifParams(options):
            try:
                conn = psycopg2.connect("dbname='" + options['database'] + "' user='" + options['postuser'] + "' host='" + options['urbanUrl'] + "' password='" + options['ropw'] + "' port='" + options['dbport'] + "'")
                conn.close()
            except psycopg2.Error as e:
                if 'could not connect to server: Connection refused' in e.message:
                    raise Exception('La connexion au serveur n\'est pas valide. Vérifier l\'adresse et le port')
                if 'FATAL:  database ' in e.message:
                    raise Exception('La nom de la basse de données n\'est pas correcte')
                if 'FATAL:  password authentication failed ' in e.message:
                    raise Exception('Erreur de login/password')
                if 'could not translate host name' in e.message:
                    raise Exception('Erreur sur l\'adresse de la base de données')
                raise Exception('Erreur de connection à la base de données')

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
