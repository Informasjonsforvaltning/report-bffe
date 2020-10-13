import os
from datetime import datetime
from typing import List

from elasticsearch import Elasticsearch

ES_HOST = os.getenv("ELASTIC_HOST", "localhost")
ES_PORT = os.getenv("ELASTIC_PORT", "9200")
es_client = Elasticsearch([ES_HOST + ":" + ES_PORT])


def get_all_update_entries() -> List[dict]:
    updates = es_client.search(
        index="updates",
        body={"query": {"match_all": {}}, "sort": [{"end_time": {"order": "desc"}}]},
    )
    update_list = [hit["_source"] for hit in updates["hits"]["hits"]]
    response = []
    for update in update_list:
        end_time = datetime.strptime(update["end_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
        start_time = datetime.strptime(update["start_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
        response.append(
            {
                "start_time": start_time.strftime("%H:%M:%S | %d.%m.%Y"),
                "end_time": end_time.strftime("%H:%M:%S | %d.%m.%Y"),
                "status": update["status"],
            }
        )

    return response
