# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from optparse import OptionParser
from optparse import make_option
from adminimio.models import Im

class Command(BaseCommand):

    args = 'params'
    help = 'Collect layer from Database'
    option_list = BaseCommand.option_list + (
    make_option("-u", "--username",
        action='store',
        type="string",
        dest='username',
        default="admin",
        help="Nom utilisateur communal"),
    )+ (
    make_option("-c", "--commune",
        action='store',
        type="string",
        dest='commune',
        default="",
        help="nom de la commune"),
    )

    def handle(self, *args, **options):
        user_name = options['username']
        comm_name = options['commune']
        result = Im.crea_group_with_manager_and_user(user_name,comm_name)

        if result:
            print("Ok")
        else:
            raise CommandError("Creation failed")
