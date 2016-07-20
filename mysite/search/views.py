from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.core.context_processors import csrf
from django.conf import settings
from django.core.cache import cache
from django.views.generic import View
from django_redis import get_redis_connection
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
import os
import urllib
import pycurl
import StringIO

def GetTrans(word):
    url =   'https://www.googleapis.com/language/translate/v2?'
    url +=  str('q='+word)
    url +=  str('&target=zh-TW')
    url +=  str('&key='+settings.GOOGLE_TRANS_API_KEY)

    curl = pycurl.Curl()
    b = StringIO.StringIO()
    curl.setopt( pycurl.URL , url )
    curl.setopt( pycurl.FOLLOWLOCATION , True )
    curl.setopt( pycurl.WRITEFUNCTION, b.write)
    curl.perform()
    res = b.getvalue()
    curl.close()
    try:
        json.loads(res)
        return res
    except ValueError:
        return ''
        
# Create your views here.
def search_from_cache(key):
    if key != "":
        value = cache.keys(str(key)+"*")

    if value != None:
        data = json.dumps(value)
        return data
    else:
        data = None
        return ''

#read cache user id
def read_from_cache(key):
    value = cache.get(str(key))
    if value == None:
        data = {}
    else:
        data = json.loads(value)
    return data

#write cache user id
def write_to_cache(obj):
    key = obj["key"]
    cache.set(str(key), json.dumps(obj), settings.NEVER_REDIS_TIMEOUT)

def dropsearch(request):
    if request.method == 'POST' and request.is_ajax():
        word = request.POST["word"]

        startT = datetime.datetime.now()
        result = search_from_cache(word)
        endT = datetime.datetime.now()

        data = {
            "status"    :   "100" ,
            "count"     :   len(result),
            "word"      :   word,
            "search_q"  :   str('*:'+word+'*'),
            "qtime"     :   str(int((endT - startT).microseconds)/1000)+"ms",
            "result"    :   result,
        }
        #Returning same data back to browser.It is not possible with Normal submit
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404()

def search(request):
    try:
        startT = datetime.datetime.now()
        if request.method == 'GET':

            response = {
                'type'  :   'GET',
                'date'  :   str(datetime.date.today().strftime("%B %d, %Y")),
            }

        if request.method == 'POST':
            word    = request.POST["tags"]
            data    = read_from_cache(word)
            endT = datetime.datetime.now()
            trans   = GetTrans(word)
            response = {
                'type'          :   'POST',
                'date'          :   str(datetime.date.today().strftime("%B %d, %Y")),
                'data'          :   data,
                'google_trans'  :   trans,
            }

        endT = datetime.datetime.now()
        pTime = endT - startT
        response.update({'time' :   str(int(pTime.microseconds)/1000)})
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
