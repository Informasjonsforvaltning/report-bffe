import asyncio
import logging
from typing import List
import traceback

from fdk_reports_bff.elasticsearch.queries import CONCEPT_AGGREGATION_FIELDS
from fdk_reports_bff.elasticsearch.utils import (
    add_org_paths_to_document,
    elasticsearch_ingest,
    get_all_organizations_with_publisher,
    get_unique_records,
)
from fdk_reports_bff.service_requests import (
    fetch_all_concepts,
    fetch_concept_publishers,
)
from fdk_reports_bff.utils import FetchFromServiceException, ServiceKey


def insert_concepts(success_status, failed_status):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        concept_tasks = asyncio.gather(fetch_all_concepts(), fetch_concept_publishers())
        concepts, publishers = loop.run_until_complete(concept_tasks)

        prepared_docs = loop.run_until_complete(
            prepare_documents(documents=concepts, publishers=publishers)
        )

        elasticsearch_ingest(index_key=ServiceKey.CONCEPTS, documents=prepared_docs)
        return success_status

    except FetchFromServiceException as err:
        logging.error(f"{traceback.format_exc()} {err.reason}")
        return failed_status


async def prepare_documents(documents: dict, publishers) -> List[dict]:
    unique_record_items = get_unique_records(documents)

    await get_all_organizations_with_publisher(publishers)
    concepts_with_fdk_portal_paths = await asyncio.gather(
        *[add_org_paths_to_document(rdf_values=entry) for entry in unique_record_items]
    )

    return [
        reduce_concept(concept=concept) for concept in concepts_with_fdk_portal_paths
    ]


def reduce_concept(concept: dict):
    reduced_dict = concept.copy()
    for items in concept.items():
        key = items[0]
        if key not in CONCEPT_AGGREGATION_FIELDS:
            reduced_dict.pop(key)
    return reduced_dict
