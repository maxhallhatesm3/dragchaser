import sys

from elasticsearch import Elasticsearch

es = Elasticsearch()

with open(sys.argv[1], 'r') as datafil:
    for datline in datafil.readlines():
        es.index(index='rpdr_powerranking', body=datline, doc_type='_doc', pipeline='rpdr_powerranking-pipeline')
