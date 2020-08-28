import datetime
import logging
import os
import atexit
from time import sleep

import elasticsearch
from apscheduler.schedulers.background import BackgroundScheduler

import pytz
from elasticsearch import NotFoundError, Elasticsearch
from urllib3.exceptions import NewConnectionError

from src.elasticsearch.datasets import insert_datasets

ES_HOST = os.getenv('ELASTIC_HOST', 'localhost')
ES_PORT = os.getenv('ELASTIC_PORT', '9200')
es_client = Elasticsearch([ES_HOST + ':' + ES_PORT])
update_interval = 2 * 60 * 60


def schedule_updates():
    scheduler = BackgroundScheduler()
    sleep(5)
    if not Update.is_running():
        Update.start_update()
        scheduler.add_job(func=Update.start_update, trigger="interval", seconds=update_interval)
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())
    return True


class Update:
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"
    ES_INDEX = "update"

    def __init__(self):
        self.status = Update.IN_PROGRESS
        self.start_time = self.get_local_time()
        self.end_time = None
        self.id = None

    @staticmethod
    def start_update(connection_attempts=0):
        if connection_attempts == 4:
            return
        update = Update()
        try:
            jobs_completed_for_intervall = es_client.search(index="updates", body=updates_last_x_minutes_query)
            if jobs_completed_for_intervall["hits"]["total"]["value"] > 0:
                return False
        except NotFoundError:
            pass
        except (elasticsearch.exceptions.ConnectionError, ConnectionRefusedError, NewConnectionError):
            sleep(5)
            Update.start_update(connection_attempts + 1)
        result = es_client.index(index="updates", body=update.doc())
        doc_id = result["_id"]
        insert_datasets(Update.cancel_update)
        Update.complete_update(doc_id, update)

    @staticmethod
    def complete_update(doc_id, update_obj):
        update_obj.end_time = Update.get_local_time()
        update_obj.status = Update.COMPLETED
        es_client.delete(index="updates", id=doc_id)
        es_client.index(index="updates", body=update_obj.doc())

    @staticmethod
    def is_running(connection_attempts=0):
        if connection_attempts == 4:
            return False
        try:
            jobs_in_progress = es_client.search(index="updates", body=in_progress_query)
            return jobs_in_progress["hits"]["total"]["value"] > 0
        except NotFoundError:
            return False
        except (elasticsearch.exceptions.ConnectionError, ConnectionRefusedError, NewConnectionError):
            logging.error(f"Connection error checking for jobs in progress. Attempts: {connection_attempts}")
            sleep(5)
            return Update.is_running(connection_attempts + 1)

    def doc(self):
        doc = {
            "status": self.status,
            "start_time": self.start_time
        }
        if self.end_time:
            doc["end_time"] = self.end_time
        return doc

    @staticmethod
    def get_local_time():
        local_tz = pytz.timezone('Europe/Oslo')
        return datetime.datetime.now(tz=local_tz)

    @staticmethod
    def scheduled() -> bool:
        try:
            es_client.search(index="updates", body=in_progress_query)
            return True
        except NotFoundError:
            return False

    @staticmethod
    def cancel_update():
        jobs_in_progress = es_client.search(index="updates", body=in_progress_query)
        for job in jobs_in_progress["hits"]["hits"]:
            es_client.delete(index="updates", id=job["_id"])


in_progress_query = {
    "query": {
        "term": {
            "status.keyword": "in progress"
        }
    }
}
updates_last_x_minutes_query = {
    "query": {
        "range": {
            "end_time": {
                "time_zone": "+01:00",
                "gte": f"now-{update_interval}m/m",
                "lte": "now"
            }
        }
    }
}
