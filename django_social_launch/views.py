# -names 	TODO

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render
from models import *
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
	return render(request, 'social_launch/index.html')
