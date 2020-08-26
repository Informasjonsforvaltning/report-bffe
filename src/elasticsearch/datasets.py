import asyncio
import logging
from src.elasticsearch.queries import DATASET_AGGREGATION_FIELDS, CATALOG_RECORD_AGGREGATION_FIELDS
from src.elasticsearch.utils import elasticsearch_ingest, add_foaf_agent_to_organization_store, \
    add_org_path_to_document, add_key_as_node_uri, EsMappings, get_values_from_nested_dict
from src.rdf_namespaces import JSON_LD
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
    documents_list = list(documents.items())
    with_mapped_node_uri = [add_key_as_node_uri(value=entry[1], key=entry[0]) for entry in documents_list]
    datasets = [entry for entry in with_mapped_node_uri if
                JSON_LD.rdf_type_equals(JSON_LD.DCAT.dataset, entry)]
    foaf_agents = [{entry[0]: entry[1]} for entry in documents_list if
                   JSON_LD.rdf_type_equals(JSON_LD.FOAF.agent, entry)]
    records = [{entry[0]: entry[1]} for entry in documents_list if
               JSON_LD.rdf_type_equals(JSON_LD.DCAT.CatalogRecord, entry)]
    distributions = [{entry[0]: entry[1]} for entry in documents_list if
                     JSON_LD.rdf_type_equals(JSON_LD.DCAT.distribution_type, entry)]

    # add foaf agents to organization store
    foaf_agents_tasks = asyncio.gather(*[add_foaf_agent_to_organization_store(agent) for agent in foaf_agents])
    await foaf_agents_tasks

    # add organization references to entry
    with_orgpath = await asyncio.gather(*[add_org_path_to_document(entry) for entry in datasets])

    # TODO lospath
    # TODO add first harvested
    return [merge_dataset_information(dataset=dataset, distributions=distributions, records=records)
            for dataset in datasets]


def merge_dataset_information(dataset, distributions, records) -> dict:
    dataset_record = [reduce_record(record) for record in records if
                      JSON_LD.node_rdf_property_equals(rdf_property=JSON_LD.FOAF.primaryTopic,
                                                       equals_value=dataset[EsMappings.NODE_URI],
                                                       entry=record
                                                       )]
    dataset[EsMappings.RECORD] = dataset_record[0]

    if dataset.get(JSON_LD.DCAT.distribution):
        dataset_distribution_node_refs = [entry.get("value") for entry in dataset[JSON_LD.DCAT.distribution]]
        dataset_distribution_values = [entry.get(JSON_LD.RDF.type) for entry in dataset[JSON_LD.DCAT.distribution]]
        ref_distribution_values = [get_values_from_nested_dict(node) for node in distributions
                                   if JSON_LD.node_uri_in(node, dataset_distribution_node_refs)]
        dataset[JSON_LD.DCAT.distribution] = [dist for dist in dataset_distribution_values + ref_distribution_values if
                                              dist]

    return reduce_dataset(dataset)


def reduce_dataset(dataset: dict):
    reduced_dict = dataset.copy()
    for items in dataset.items():
        key = items[0]
        if key not in DATASET_AGGREGATION_FIELDS:
            reduced_dict.pop(key)
    return reduced_dict


def reduce_record(record: dict):
    record_values = get_values_from_nested_dict(record)
    reduced_record = record_values.copy()
    for items in record_values.items():
        key = items[0]
        if key not in CATALOG_RECORD_AGGREGATION_FIELDS:
            reduced_record.pop(key)
    return reduced_record


def perform_datasets_aggregation_query():
    pass
