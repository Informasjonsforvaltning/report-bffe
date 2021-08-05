from datetime import datetime
import os
from typing import List

from elasticsearch import Elasticsearch

ES_HOST = os.getenv("ELASTIC_HOST", "localhost")
ES_PORT = os.getenv("ELASTIC_PORT", "9200")
es_client = Elasticsearch([ES_HOST + ":" + ES_PORT])


def get_all_update_entries() -> List[dict]:
    updates = es_client.search(
        size="100",
        index="updates",
        body={"query": {"match_all": {}}, "sort": [{"start_time": {"order": "desc"}}]},
    )
    update_list = [hit["_source"] for hit in updates["hits"]["hits"]]
    response = []
    for update in update_list:
        end_time = (
            datetime.strptime(update["end_time"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
                "%H:%M:%S | %d.%m.%Y"
            )
            if "end_time" in update
            else ""
        )
        start_time = (
            datetime.strptime(update["start_time"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime(
                "%H:%M:%S | %d.%m.%Y"
            )
            if "start_time" in update
            else ""
        )
        response.append(
            {
                "start_time": start_time,
                "end_time": end_time,
                "status": update["status"],
            }
        )

    return response
