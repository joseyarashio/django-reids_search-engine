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

def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hello_world(request):
    return render(request, 'hello_world.html', {
        'cookie': str(datetime.date.today().strftime("%B %d, %Y")),
    })

def show(request,pk):
    return render(request, 'show.html', {'post',str(pk)})
    # print("1")

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    if post is not None:
        return render(request, 'post.html', {'post': post})
    else:
        return render(request, 'show.html', {'post': null})

def test(request):
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
                'static'    :   settings.STATIC_URL
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
