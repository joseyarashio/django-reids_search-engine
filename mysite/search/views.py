from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.conf import settings
from django.core.cache import cache
from django.views.generic import View
from .models import Post
from django_redis import get_redis_connection
import datetime
import json

# Create your views here.
#read cache user id
def read_from_cache(user_name):
    key = 'user_id_of_'+user_name
    value = cache.get(key)
    if value == None:
        data = None
    else:
        data = json.loads(value)
    return data

#write cache user id
def write_to_cache(user_name):
    key = 'user_id_of_'+user_name
    cache.set(key, json.dumps(user_name), settings.NEVER_REDIS_TIMEOUT)

def search(request):
    try:
        if request.method == 'GET':
            session  = request.session
            cookie   = request.COOKIES.get('logged_in_status')
            ip = get_client_ip(request)

            # read from redis cache
            access_hist = read_from_cache(str(ip))

            response = render(request, 'hello_world.html', {
                'cookie': str(cookie),
                'ip'    : str(ip),
                'date'  : str(datetime.date.today().strftime("%B %d, %Y")),
                'access_hist'  : access_hist,
            })

            # write to  redis cache
            write_to_cache(str(ip))

            set_cookie(response,'logged_in_status',"123",7)
            # get_redis_connection("default")
        return response

    except TypeError:
        raise Http404()

    except ValueError:
        raise Http404()