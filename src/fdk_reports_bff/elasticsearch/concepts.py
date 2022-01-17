import asyncio
import logging
import traceback
from typing import List

from fdk_reports_bff.elasticsearch.queries import (
    CONCEPT_AGGREGATION_FIELDS,
    EsMappings,
)
from fdk_reports_bff.elasticsearch.utils import (
    elasticsearch_ingest,
    get_unique_records,
)
from fdk_reports_bff.service.service_requests import fetch_all_concepts
from fdk_reports_bff.service.utils import FetchFromServiceException, ServiceKey


def insert_concepts(success_status: str, failed_status: str) -> str:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        concept_tasks = asyncio.gather(fetch_all_concepts())
        concepts = loop.run_until_complete(concept_tasks)[0]

        prepared_docs = loop.run_until_complete(prepare_documents(documents=concepts))

        elasticsearch_ingest(index_key=ServiceKey.CONCEPTS, documents=prepared_docs)
        return success_status

    except FetchFromServiceException as err:
        logging.error(f"{traceback.format_exc()} {err.reason}")
        return failed_status


async def prepare_documents(documents: List[dict]) -> List[dict]:
    unique_record_items = get_unique_records(documents)

    return [reduce_concept(concept=concept) for concept in unique_record_items]


def reduce_concept(concept: dict) -> dict:
    reduced_dict = concept.copy()
    for items in concept.items():
        key = items[0]
        if key not in CONCEPT_AGGREGATION_FIELDS:
            reduced_dict.pop(key)
        elif key in EsMappings.ORG_PATH or key in EsMappings.ORGANIZATION_ID:
            reduced_dict[key] = concept[key]["value"]
    return reduced_dict
