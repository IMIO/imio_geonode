from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.gis.geos import Polygon
from imio_survey.tasks import doSurvey


def index(request):
	poly = Polygon( ((121000, 126000), (121000, 126100), (121100, 126100), (121100, 126000), (121000, 126000)) )
	result = doSurvey("TEST", poly.wkt)

	return render(request, 'imio_survey/index.html', {
		'survey_result' : result
	})

def post_survey(request):
	pass

def get_survey(request):
	pass

def get_survey_list(request):
	pass
