# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf import settings
from django.views.generic import TemplateView



urlpatterns = patterns(
    'adminimio.views',
    #url(r'^$', TemplateView.as_view(template_name='adminimio/imio_management.html'), name='imio_management'),
    url(r'^$', 'admin_view_imio', name='imio_management'),
    url(r'^updatelayer$', 'admin_view_updatelayer', name='imio_management_updatelayer'),
    url(r'^commune$', 'admin_view_crea_group_with_manager', name='imio_management_commune'),
    url(r'^addurb$', 'admin_view_addurb', name='imio_management_addurb'),
    #url(r'^commune/action$', 'admin_view_crea_group_with_manager_action', name='imio_management_commune_action'),
)
