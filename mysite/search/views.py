from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.conf import settings
from django.core.cache import cache
from django.views.generic import View
from django_redis import get_redis_connection
import datetime
import json
import os

# Create your views here.
#read cache user id
def read_from_cache(user_name):
    key = user_name
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
    cache.set(key, json.dumps(obj), settings.NEVER_REDIS_TIMEOUT)

def search(request):
    try:
        if request.method == 'GET':

            # read from redis cache
            access_hist = read_from_cache("")

            response = render(request, 'search.html', {
                # 'cookie': str(cookie),
                'date'  : str(datetime.date.today().strftime("%B %d, %Y")),
                'access_hist'  : access_hist,
            })

            # write to  redis cache
            # write_to_cache(str(ip))

            # get_redis_connection("default")
        return response

    except TypeError:
        raise Http404()

    except ValueError:
        raise Http404()
def writeall(request):
    os.chdir(r'/home/johnny/djangogirls/mysite/search')
    with open("dict.txt", "r") as f:
        lines = f.readlines()
        # read from redis cache
        access_hist = read_from_cache("")
        obj = {
            'key'   :   lines[12333].replace('\n', ''),
            'ins_date'  : str(datetime.date.today().strftime("%B %d, %Y")),
        }
        write_to_cache(obj)
        response = render(request, 'search.html', {
            # 'cookie': str(cookie),
            'date'  : str(datetime.date.today().strftime("%B %d, %Y")),
            'dict'  : lines[1234],
        })

        # write to  redis cache
        # write_to_cache(str(ip))
        # get_redis_connection("default")
        return response
