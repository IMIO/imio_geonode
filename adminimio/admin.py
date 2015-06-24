# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.management import call_command
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns
from adminimio.models import Im

class ImAdmin(admin.ModelAdmin):
    pass

def update_layer_from_geoserver(modeladmin, request, queryset):
    call_command('updatelayers')

admin.site.add_action(update_layer_from_geoserver, 'Update layer from Geoserver')
admin.site.register(Im,ImAdmin)
