import os
from elasticsearch import Elasticsearch

from src.rdf_namespaces import DCAT, NamespaceProperty

ES_HOST = os.getenv('ELASTIC_HOST', 'localhost')
ES_PORT = os.getenv('ELASTIC_PORT', '9200')
es_client = Elasticsearch([ES_HOST + ':' + ES_PORT])
