import asyncio
import logging

from src.service_requests import fetch_all_concepts
from src.utils import FetchFromServiceException, ServiceKey
from src.elasticsearch.utils import elasticsearch_ingest, EsMappings
from src.organization_parser import OrganizationReferencesObject


def insert_concepts(success_status, failed_status):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        concepts = loop.run_until_complete(fetch_all_concepts())

        concepts = [add_es_aggregation_fields(concept=concept)
                             for concept in concepts]

        elasticsearch_ingest(ServiceKey.CONCEPTS, concepts)
        return success_status

    except FetchFromServiceException as err:
        logging.error(err.reason)
        return failed_status


def add_es_aggregation_fields(concept) -> dict:
    if concept.get(EsMappings.PUBLISHER):
        concept[EsMappings.ORG_PATH] = concept[EsMappings.PUBLISHER][EsMappings.ORG_PATH]
        concept[EsMappings.ORGANIZATION_ID] = OrganizationReferencesObject.resolve_id(
            concept[EsMappings.PUBLISHER][EsMappings.URI])
    return concept
