import sys
import json

from elasticsearch import Elasticsearch

es = Elasticsearch()

with open('db2.json', 'r') as deeb:
    queen_db = json.load(deeb)

with open(sys.argv[1], 'r') as datafil:
    for datline in datafil.readlines():
        servdat = json.loads(datline)
        queen = queen_db.get(servdat.get('name'))
        servdat.update(queen)
        es.index(index='rpdr_powerranking', body=servdat, doc_type='_doc', pipeline='rpdr_powerranking-pipeline')
