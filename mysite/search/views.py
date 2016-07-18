from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.core.context_processors import csrf
from django.conf import settings
from django.core.cache import cache
from django.views.generic import View
from django_redis import get_redis_connection
import datetime
import json
import os

# Create your views here.
#read cache user id
def read_from_cache(key):

    value = cache.keys(key)

    if value == None:
        data = None
    else:
        data = ''
        # data = json.loads(value)
    return data

#write cache user id
def write_to_cache(obj):
    key = obj["key"]

    cache.set(str(key), json.dumps(obj), settings.NEVER_REDIS_TIMEOUT)

def search(request):
    try:
        startT = datetime.datetime.now()
        if request.method == 'GET':

            response = {
                'type'  :   'GET',
                'date'  :   str(datetime.date.today().strftime("%B %d, %Y")),
            }

        if request.method == 'POST':
            text = request.POST["tags"]
            data = read_from_cache(':'+text+'*')
            response = {
                'type'  :   'POST',
                'date'  :   str(datetime.date.today().strftime("%B %d, %Y")),
                'data'  :   data,
            }

        endT = datetime.datetime.now()
        pTime = endT - startT
        response.update({'time' :   pTime.microseconds})
        # Improttant
        response.update(csrf(request))
        return render(request, 'search.html', response)

    except TypeError:
        raise Http404()

    except ValueError:
        raise Http404()
def writeall(request):
    startT = datetime.datetime.now()
    os.chdir(r'/home/johnny/djangogirls/mysite/search')
    with open("dict.txt", "r") as f:
        lines = f.readlines()
        # read from redis cache
        for item in lines:
            obj = {
                'key'   :   item.replace('\n', ''),
                'ins_date'  : str(datetime.date.today().strftime("%B %d, %Y")),
            }
            write_to_cache(obj)
            # cache.set("fsdf", "fasdff", None)

        endT = datetime.datetime.now()
        pTime = endT - startT
        response = render(request, 'search.html', {
            # 'cookie': str(cookie),
            'date'  :   str(datetime.date.today().strftime("%B %d, %Y")),
            'dict'  :   obj["key"],
            'time'  :   pTime.microseconds
        })


        # write to  redis cache
        # write_to_cache(str(ip))
        # get_redis_connection("default")
        return response
