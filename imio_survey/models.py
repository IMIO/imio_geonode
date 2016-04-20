from django.db import models

class SurveyResult():
    def __init__(self, name, features):
        self.name = name
        self.features = features

class SurveyGisServer(models.Model):
    OGC = 'OGC'
    ARCREST = 'ARCREST'
    GEONODE = 'GEONODE'
    GISSERVER_TYPES = (
        (OGC, 'OGC WMS/WFS Server'),
        (ARCREST, 'Arcgis Server REST API'),
        (GEONODE, 'Imio Geonode Local Instance'),
    )
    url = models.CharField(max_length=200,primary_key=True)
    servertype = models.CharField(max_length=7, choices=GISSERVER_TYPES)
    description = models.CharField(max_length=250)
    username = models.CharField(max_length=100,blank=True,null=True)
    password = models.CharField(max_length=100,blank=True,null=True)

    def __unicode__(self):              # __str__ on Python 3
        return self.description

class SurveyLayer(models.Model):
    description = models.CharField(max_length=200)
    layer_name = models.CharField(max_length=200)
    gis_server = models.ForeignKey(SurveyGisServer)
    geometry_field_name = models.CharField(max_length=50)
    def __unicode__(self):              # __str__ on Python 3
        return self.description

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
    def __unicode__(self):              # __str__ on Python 3
        return str(self.survey_type) + ":" + str(self.survey_layer)
