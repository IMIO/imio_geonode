# -*- coding: utf-8 -*-

from django.conf.urls import url

from imio_survey import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
