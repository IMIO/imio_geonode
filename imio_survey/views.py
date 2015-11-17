from django.shortcuts import render
from django.http import HttpResponse
from imio_survey.tasks import doSurvey

def index(request):
	return render(request, 'imio_survey/index.html')

def post_survey(request):
	pass

def get_survey(request):
	pass

def get_survey_list(request):
	pass
