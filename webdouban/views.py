#__author__ = 'zjh'
from django.http import HttpResponseRedirect

def index(request):
    return HttpResponseRedirect('/auth/index/')