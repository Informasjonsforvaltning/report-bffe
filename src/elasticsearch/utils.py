import json
import logging
import os
from typing import List

from elasticsearch import helpers
from elasticsearch.helpers import BulkIndexError

from src.elasticsearch import es_client
from src.elasticsearch.queries import EsMappings, AggregationQuery, TimeSeriesQuery
from src.organization_parser import OrganizationStore, OrganizationReferencesObject, \
    OrganizationStoreNotInitiatedException
from src.rdf_namespaces import JSON_RDF
from src.referenced_data_store import get_organizations, get_los_path, get_organization
from src.utils import ServiceKey, ContentKeys


def add_key_as_node_uri(key, value):
    value[EsMappings.NODE_URI] = key
    return value


async def get_all_organizations_with_publisher(publishers):
    await get_organizations()
    OrganizationStore.get_instance().add_all_publishers(publishers)


async def add_org_and_los_paths_to_document(json_rdf_values: dict, los_themes: List[dict]) -> dict:
    uri = json_rdf_values[JSON_RDF.dct.publisher][0][ContentKeys.VALUE]

    try:
        ref_object = OrganizationReferencesObject.from_dct_publisher(org_uri=uri)
        referenced_organization = await get_organization(ref_object)
        if referenced_organization:
            org_path = referenced_organization.org_path
            org_id = OrganizationReferencesObject.resolve_id(referenced_organization.org_uri)
            json_rdf_values[EsMappings.ORG_PATH] = org_path
            json_rdf_values[EsMappings.ORGANIZATION_ID] = org_id
        return add_los_path_to_document(json_rdf_values, los_themes)
    except OrganizationStoreNotInitiatedException:
        await get_organizations()
        return await add_org_and_los_paths_to_document(json_rdf_values, los_themes)


def add_los_path_to_document(json_rdf_values: dict, los_themes: List[dict]) -> dict:
    if JSON_RDF.dcat.theme in json_rdf_values.keys():
        los_uris = [theme.get(ContentKeys.VALUE) for theme in json_rdf_values.get(JSON_RDF.dcat.theme)]
        los_paths = get_los_path(uri_list=los_uris, los_themes=los_themes)
        if len(los_paths) > 0:
            json_rdf_values[EsMappings.LOS] = los_paths
    return json_rdf_values


def elasticsearch_ingest(index_key: ServiceKey, documents: List[dict]):
    recreate_index(index_key=index_key)
    try:
        result = helpers.bulk(client=es_client, index=index_key, actions=yield_documents(documents))
        return result
    except BulkIndexError as err:
        logging.error(f"ingest {ServiceKey.DATA_SETS}", err.errors)


def yield_documents(documents):
    for doc in documents:
        yield doc


def get_values_from_nested_dict(entry: dict) -> dict:
    root_key = list(entry.keys())[0]
    return entry[root_key]


# noinspection PyBroadException
def recreate_index(index_key):
    """delete and recreate an index with settings and mapping from file"""
    logging.info("reindexing {0}".format(index_key))
    with open(os.getcwd() + "/mapping/{0}_properties.json".format(index_key)) as mapping:
        try:
            es_client.indices.delete(index=index_key, ignore=[400, 404])
            es_client.indices.create(index=index_key, body=json.load(mapping))
        except BaseException as err:
            logging.error("error when attempting to update {0} ".format(index_key))
        return None


def elasticsearch_get_report_aggregations(report_type: ServiceKey, orgpath=None, theme=None,
                                          theme_profile=None, organization_id=None):
    query = AggregationQuery(report_type=report_type,
                             orgpath=orgpath,
                             theme=theme,
                             theme_profile=theme_profile,
                             organization_id=organization_id).build()
    aggregations = es_client.search(index=report_type, body=query)
    return aggregations


def elasticsearch_get_time_series(report_type: ServiceKey, org_path=None, theme=None,
                                  theme_profile=None, organization_id=None):
    query = TimeSeriesQuery(orgpath=org_path, theme_profile=theme_profile, theme=theme,
                            organization_id=organization_id).build()
    aggregations = es_client.search(index=report_type, body=query)
    return aggregations
