import asyncio
import logging
from typing import List

from src.elasticsearch.utils import elasticsearch_ingest, add_foaf_agent_to_organization_store, \
    add_org_path_to_document, add_key_as_node_uri
from src.rdf_namespaces import JSON_LD, ContentKeys
from src.service_requests import fetch_catalog_from_dataset_harvester
from src.utils import FetchFromServiceException, ServiceKey


def insert_datasets():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        dataset_rdf = loop.run_until_complete(fetch_catalog_from_dataset_harvester())
        prepared_docs = loop.run_until_complete(prepare_documents(dataset_rdf))
        elasticsearch_ingest(index_key=ServiceKey.DATA_SETS, documents=prepared_docs)
    except FetchFromServiceException as err:
        logging.error(err.reason)
        return


async def prepare_documents(documents: dict) -> dict:
    # TODO add metadata?
    documents_list = list(documents.items())
    with_node_uri = [add_key_as_node_uri(value=entry[1], key=entry[0]) for entry in documents_list]
    datasets = [entry for entry in with_node_uri if
                JSON_LD.rdf_type_equals(JSON_LD.DCAT.dataset, entry)]
    foaf_agents = [{entry[0]: entry[1]} for entry in documents_list if
                   JSON_LD.rdf_type_equals(JSON_LD.FOAF.agent, entry)]
    # add foaf agents to organization store
    foaf_agents_tasks = asyncio.gather(*[add_foaf_agent_to_organization_store(agent) for agent in foaf_agents])
    await foaf_agents_tasks

    # add organization references to entry
    with_orgpath = await asyncio.gather(*[add_org_path_to_document(entry) for entry in datasets])

    # with_org_and_los_path = loop.run_until_complete(
    #    asyncio.gather([add_los_path_to_entry(dataset) for dataset in with_orgpath])
    # )
    return with_orgpath


def perform_datasets_aggregation_query():
    pass
