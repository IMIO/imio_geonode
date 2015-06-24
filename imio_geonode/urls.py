from django.conf.urls import patterns, url

from geonode.urls import *

urlpatterns = patterns('',

    # Static pages
    url(r'^$', TemplateView.as_view(template_name='site_index.html'), name='home'),

    # Imio
    (r'^adminimio/', include('adminimio.urls')),
 ) + urlpatterns
