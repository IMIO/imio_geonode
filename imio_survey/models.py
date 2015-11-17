from django.db import models

GISSERVER_TYPES = (
    ('OGC', 'OGC WMS/WFS Server'),
    ('ARCREST', 'Arcgis Server REST API'),
)

class SurveyType(models.Model):
    key = models.CharField(max_length=200,primary_key=True)
    description = models.CharField(max_length=200, null=True)
    survey_layers = models.ManyToManyField(SurveyLayer, through='SurveyTypeLayer')

    def __unicode__(self):              # __str__ on Python 3
        return self.key

class SurveyTypeLayer(models.Model):
    survey_type = models.ForeignKey(SurveyType)
    survey_layer = models.ForeignKey(SurveyLayer)
    buffer = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)

class SurveyLayer(models.Model):
    layer_name = models.CharField(max_length=200,primary_key=True)
    gis_server = models.ForeignKey(SurveyGisServer)

    def __unicode__(self):              # __str__ on Python 3
        return self.layer_name

class SurveyGisServer(models.Model):
    url = models.CharField(max_length=200,primary_key=True)
    servertype = models.CharField(max_length=7, choices=GISSERVER_TYPES)
    description = models.CharField(max_length=250, null=True)
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)

    def __unicode__(self):              # __str__ on Python 3
        return self.url
