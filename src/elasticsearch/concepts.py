import asyncio
import logging

from src.service_requests import fetch_all_concepts
from src.utils import FetchFromServiceException, ServiceKey
from src.elasticsearch.utils import elasticsearch_ingest


def insert_concepts():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        concepts = loop.run_until_complete(fetch_all_concepts())
        elasticsearch_ingest(ServiceKey.CONCEPTS, concepts)

    except FetchFromServiceException as err:
        logging.error(err.reason)