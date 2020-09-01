import os
from typing import List

from elasticsearch import Elasticsearch

from src.rdf_namespaces import DCAT, NamespaceProperty

ES_HOST = os.getenv('ELASTIC_HOST', 'localhost')
ES_PORT = os.getenv('ELASTIC_PORT', '9200')
es_client = Elasticsearch([ES_HOST + ':' + ES_PORT])


def get_all_update_entries() -> List[dict]:
    updates = es_client.search(index="updates", body={
        "query": {
            "match_all": {}
        }
    })

    update_list = [hit["_source"] for hit in updates["hits"]["hits"]]
    return update_list
