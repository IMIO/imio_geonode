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
    )

    #parser = OptionParser()
    #parser.add_option("-p", "--gpw", action="store", type="string", dest="gpw", default="", help="Geoserver admin password [default: %default]")
    #parser.add_option("-u", "--urbanUrl", action="store", type="string", dest="urbanUrl", default="", help="Urban URL [default: %default]")
    #parser.add_option("-r", "--ropw", action="store", type="string", dest="ropw", default="", help="Remote postGIS ro_user password [default: %default]")
    #parser.add_option("-d", "--database", action="store", type="string", dest="database", default="urb_xxx", help="remote urban database name [default: %default]")
    #parser.add_option("-a", "--alias", action="store", type="string", dest="alias", default="", help="prefix alias [default: %default]")
    #parser.add_option("-z", "--uri", action="store", type="string", dest="uri", default="imio.be", help="uri= [default: %default]")
    #parser.add_option("-g", "--postuser", action="store", type="string", dest="postuser", default="ro_user", help="db_use r= [default: %default]")
    #parser.add_option("-c", "--geoserveradmin", action="store", type="string", dest="geoserveradmin", default="admin", help="Geoserver admin = [default: %default]")
    #(options, args) = parser.parse_args()
    #if options.gpw is None:
    #    parser.error('Admin geoserver password not given')
    #if options.urbanUrl is None:
    #    parser.error('Urban postGIS URL not given')
    #if options.ropw is None:
    #    parser.error('database password not given')
    #if options.alias is None:
    #    parser.error('alias not given')
    
    def handle(self, *args, **options):

        #connect to geoserver
        cat = Catalog("http://localhost:8080/geoserver/rest", options['geoserveradmin'], options['gpw'])

        #create datrastore for URB schema
        ws = cat.create_workspace(options['alias'],options['uri'])

        ds = cat.create_datastore(options['alias'], ws)
        ds.connection_parameters.update(
            host=options['urbanUrl'],
            port="5432",
            database=options['database'],
            user=options['postuser'],
            passwd=options['ropw'],
            dbtype="postgis")

        cat.save(ds)
        ds = cat.get_store(options['alias'])

        #config object
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

        try:
            #connect to tables and create layers and correct urban styles
            print("premiere boucle")
            for table in urb:

                # push data in geoserver
                style = urb[table]
                ft = cat.publish_featuretype(table, ds, 'EPSG:31370', srs='EPSG:31370')
                ft.default_style = style
                cat.save(ft)
                res_name = ft.dirty['name']
                res_title = options['alias']+"_"+table

            print("2iem boucle")
            for table in urb:

                # rename layer
#               layer, created = Layer.objects.get_or_create(name=res_name, defaults={
#                   "workspace": ws.name,
#                   "store": ds.name,
#                   "storeType": ds.resource_type,
#                   "typename": "%s:%s" % (ws.name.encode('utf-8'), res_name.encode('utf-8')),
#                   "title": res_title or 'No title provided',
#                   "abstract": 'No abstract provided',
#                   #"owner": owner,
#                   "uuid": str(uuid4())
#                   #"bbox_x0": Decimal(ft.latLonBoundingBox.miny),
#                   #"bbox_x1": Decimal(ft.latLonBoundingBox.maxy),
#                   #"bbox_y0": Decimal(ft.latLonBoundingBox.minx),
#                   #"bbox_y1": Decimal(ft.latLonBoundingBox.maxx)
#                   })

                if created:
                    layer.set_default_permissions()
                    layer.save()
                else:
                    print("   !!! le layer n'as pas ete cree ... Verifier si il etait deja cree avant ?")
        except Exception as e:
            print(str(e))

        call_command('updatelayers')
