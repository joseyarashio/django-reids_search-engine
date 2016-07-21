from elasticsearch import Elasticsearch
import datetime
import json

class EsearchTool():
    SEARCH_HOST = '127.0.0.1'
    PORT = 9200
    _INDEX = "dict"
    _TYPE = "vocab"

    es = Elasticsearch(send_get_body_as = 'POST')

    # Constructor
    def __init__(self):
        self.es = Elasticsearch([
            {'host': self.SEARCH_HOST},
            # {'host': 'othernode', 'port': 443, 'url_prefix': 'es', 'use_ssl': True},
        ])

    # Destructor
    def __exit__(self, exc_type, exc_value, traceback):
        self.es = None

        # res = self.es.index(index = self._INDEX, doc_type = self._TYPE, id = 12049349393, body = doc)
    def index(self,id,body):
        res = self.es.index(index = self._INDEX, doc_type = self._TYPE, id = id, body = body)
        return res

    def search(self,q):
        res = self.es.search(index = self._INDEX, doc_type = self._TYPE, q = q, pretty=True)
        return json.dumps(res['hits']['hits'])
    # runmain process
    # runprocess(self)
# EsearchTool.runprocess()
