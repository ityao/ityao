import json 
import time 
from django.http import HttpResponse
from django.template import Context, loader

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template.context import RequestContext

def home(request): 
    return render_to_response(u'index.html',{}, context_instance=RequestContext(request))

def about(request): 
    return render_to_response(u'about.html')

def timestamp(request): 
    return HttpResponse(json.dumps({u'time': 1000 * time.time()}),mimetype=u'application/json')
