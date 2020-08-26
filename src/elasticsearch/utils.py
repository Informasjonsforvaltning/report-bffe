import logging
from typing import List

from elasticsearch import helpers
from elasticsearch.helpers import BulkIndexError

from src.elasticsearch import es_client
from src.organization_parser import OrganizationStore, OrganizationReferencesObject, \
    OrganizationStoreNotInitiatedException
from src.rdf_namespaces import JSON_LD, ContentKeys
from src.referenced_data_store import get_org_path, get_organizations
from src.utils import ServiceKey


class EsMappings:
    RECORD = "dcatRecord"
    VALUE_KEYWORD = ".value.keyword"
    NODE_URI = "nodeUri"
    ORG_PATH = "orgPath"
    LOS_PATH = "losPath"
    MISSING = "MISSING"


def add_key_as_node_uri(key, value):
    value[EsMappings.NODE_URI] = key
    return value


async def add_foaf_agent_to_organization_store(foaf_agent_dict: dict):
    store = OrganizationStore.get_instance()
    uri = list(foaf_agent_dict.keys())[0]
    values = foaf_agent_dict[uri]
    same_as = None
    keys = values.keys()
    if JSON_LD.OWL.sameAs in keys:
        same_as = values[JSON_LD.OWL.sameAs][0][ContentKeys.VALUE]
    name = values[JSON_LD.FOAF.name][0][ContentKeys.VALUE]
    if same_as:
        org_path = await get_org_path(uri=same_as, name=name)
    else:
        org_path = await get_org_path(uri=uri, name=name)
    store.add_organization(organization=OrganizationReferencesObject(
        org_uri=uri,
        same_as=same_as,
        org_path=org_path,
        name=name
    ))
    return True


async def add_org_path_to_document(json_ld_values: dict) -> dict:
    uri = json_ld_values[JSON_LD.DCT.publisher][0][ContentKeys.VALUE]
    store = OrganizationStore.get_instance()
    try:
        org_path = store.get_orgpath(uri)
        json_ld_values[EsMappings.ORG_PATH] = org_path
        return json_ld_values
    except OrganizationStoreNotInitiatedException:
        await get_organizations()
        return await add_org_path_to_document(json_ld_values)


def elasticsearch_ingest(index_key: ServiceKey, documents: List[dict]):
    try:
        result = helpers.bulk(client=es_client, index=index_key, actions=yield_documents(documents))
        return result
    except BulkIndexError as err:
        logging.error(f"ingest {ServiceKey.DATA_SETS}", err.errors)


def yield_documents(documents):
    # TODO add orgpath and lospath
    for doc in documents:
        yield doc


def get_values_from_nested_dict(entry: dict):
    root_key = list(entry.keys())[0]
    return entry[root_key]


def extend_and_remove_uri_reference(original_list, original_list_references, referenced_entries):
    reduced_original_list = []


    return reduced_original_list
