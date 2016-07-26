from django_redis import get_redis_connection
from django.conf import settings

class Redistool():
    #read cache user id
    def read_from_cache(key):
        data = cache.get(str(key))
        return data

    #write cache user id
    def write_to_cache(key,value):
        cache.set(key, value, settings.NEVER_REDIS_TIMEOUT)
