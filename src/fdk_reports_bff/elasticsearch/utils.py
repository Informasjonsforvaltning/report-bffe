import json
import logging
import os
import traceback
from typing import Any, List

from elasticsearch import helpers
from elasticsearch.helpers import BulkIndexError

from fdk_reports_bff.elasticsearch import es_client
from fdk_reports_bff.elasticsearch.queries import (
    AggregationQuery,
    EsMappings,
    TimeSeriesQuery,
)
from fdk_reports_bff.service.organization_parser import (
    OrganizationReferencesObject,
    OrganizationStore,
    OrganizationStoreNotInitiatedException,
)
from fdk_reports_bff.service.rdf_namespaces import JsonRDF
from fdk_reports_bff.service.referenced_data_store import (
    get_los_path,
    get_organization,
    get_organizations,
)
from fdk_reports_bff.service.utils import ContentKeys, ServiceKey


def add_key_as_node_uri(key: str, value: dict) -> dict:
    value[EsMappings.NODE_URI] = key
    return value


async def get_all_organizations_with_publisher(publishers: dict) -> None:
    await get_organizations()
    OrganizationStore.get_instance().add_all_publishers(publishers)


async def add_org_and_los_paths_to_document(
    json_rdf_values: dict, los_themes: List[dict]
) -> dict:
    uri = (
        json_rdf_values[JsonRDF.dct.publisher][0][ContentKeys.VALUE]
        if JsonRDF.dct.publisher in json_rdf_values
        else None
    )
    try:
        ref_object = OrganizationReferencesObject.from_dct_publisher(org_uri=uri)
        referenced_organization = await get_organization(ref_object)
        if referenced_organization:
            org_path = referenced_organization.org_path
            org_id = OrganizationReferencesObject.resolve_id(
                referenced_organization.org_uri
            )
            json_rdf_values[EsMappings.ORG_PATH] = org_path
            json_rdf_values[EsMappings.ORGANIZATION_ID] = org_id
        return add_los_path_to_document(json_rdf_values, los_themes)
    except OrganizationStoreNotInitiatedException:
        await get_organizations()
        return await add_org_and_los_paths_to_document(json_rdf_values, los_themes)


async def add_org_paths_to_document(rdf_values: dict) -> dict:
    if ContentKeys.SAME_AS in rdf_values.keys():
        uri = rdf_values[ContentKeys.SAME_AS][ContentKeys.VALUE]
    elif ContentKeys.PUBLISHER in rdf_values.keys():
        uri = rdf_values[ContentKeys.PUBLISHER][ContentKeys.VALUE]
    else:
        return rdf_values
    try:
        ref_object = OrganizationReferencesObject.from_dct_publisher(org_uri=uri)
        referenced_organization = await get_organization(ref_object)
        if referenced_organization:
            org_path = referenced_organization.org_path
            org_id = OrganizationReferencesObject.resolve_id(
                referenced_organization.org_uri
            )
            rdf_values[EsMappings.ORG_PATH] = org_path
            rdf_values[EsMappings.ORGANIZATION_ID] = org_id
        return rdf_values
    except OrganizationStoreNotInitiatedException:
        await get_organizations()
        return await add_org_paths_to_document(rdf_values)


async def add_formats_to_document(rdf_values: dict) -> dict:
    if EsMappings.MEDIATYPE in rdf_values.keys():
        rdf_values[EsMappings.MEDIATYPE][ContentKeys.VALUE] = [
            "https://www.iana.org/assignments/media-types/application/vnd.geo+json",
            "application/json",
        ]
    return rdf_values


def add_los_path_to_document(json_rdf_values: dict, los_themes: List[dict]) -> dict:
    if JsonRDF.dcat.theme in json_rdf_values.keys():
        themes = (
            json_rdf_values[JsonRDF.dcat.theme]
            if json_rdf_values.get(JsonRDF.dcat.theme)
            else []
        )
        los_uris = [theme.get(ContentKeys.VALUE) for theme in themes]
        los_paths = get_los_path(uri_list=los_uris, los_themes=los_themes)
        if len(los_paths) > 0:
            json_rdf_values[EsMappings.LOS] = los_paths
    return json_rdf_values


def elasticsearch_ingest(index_key: str, documents: List[dict]) -> Any:
    recreate_index(index_key=index_key)
    try:
        result = helpers.bulk(
            client=es_client, index=index_key, actions=yield_documents(documents)
        )
        return result
    except BulkIndexError:
        logging.error(f"{traceback.format_exc()} ingest {ServiceKey.DATA_SETS}")


def yield_documents(documents: list) -> Any:
    for doc in documents:
        yield doc


def get_values_from_nested_dict(entry: dict) -> dict:
    root_key = list(entry.keys())[0]
    return entry[root_key]


# noinspection PyBroadException
def recreate_index(index_key: str) -> None:
    """delete and recreate an index with settings and mapping from file"""
    logging.info("reindexing {0}".format(index_key))
    with open(
        os.getcwd() + "/mapping/{0}_properties.json".format(index_key)
    ) as mapping:
        try:
            es_client.indices.delete(index=index_key, ignore_unavailable="true")
            es_client.indices.create(index=index_key, body=json.load(mapping))
        except BaseException:
            logging.error(
                f"{traceback.format_exc()} error when attempting to update {index_key}"
            )
        return None


def elasticsearch_get_report_aggregations(
    report_type: str,
    orgpath: Any = None,
    theme: Any = None,
    theme_profile: Any = None,
    organization_id: Any = None,
) -> Any:
    query = AggregationQuery(
        report_type=report_type,
        orgpath=orgpath,
        theme=theme,
        theme_profile=theme_profile,
        organization_id=organization_id,
    ).build()
    aggregations = es_client.search(index=report_type, body=query)
    return aggregations


def elasticsearch_get_concept_report_aggregations(
    report_type: str,
    orgpath: Any = None,
    theme: Any = None,
    theme_profile: Any = None,
    organization_id: Any = None,
) -> Any:
    query_array = [
        {"index": "datasets"},
        {
            "_source": ["http://purl.org/dc/terms/subject"],
            "size": 0,
            "query": {"exists": {"field": "http://purl.org/dc/terms/subject"}},
            "aggregations": {
                "most_in_use": {
                    "terms": {
                        "field": "http://purl.org/dc/terms/subject.value.keyword",
                        "size": 5,
                    }
                }
            },
        },
        {"index": "concepts"},
    ]
    query = AggregationQuery(
        report_type=report_type,
        orgpath=orgpath,
        theme=theme,
        theme_profile=theme_profile,
        organization_id=organization_id,
    ).build()
    query_array.append(query)

    aggregations = es_client.msearch(body=query_array)
    return aggregations.get("responses")


def elasticsearch_get_time_series(
    report_type: str,
    org_path: Any = None,
    theme: Any = None,
    theme_profile: Any = None,
    organization_id: Any = None,
    series_field: Any = None,
) -> Any:
    query = TimeSeriesQuery(
        series_field,
        orgpath=org_path,
        theme_profile=theme_profile,
        theme=theme,
        organization_id=organization_id,
    ).build()
    aggregations = es_client.search(index=report_type, body=query)
    return aggregations


def get_unique_records(items: List[dict]) -> List[dict]:
    seen = set()
    unique_records = []
    for obj in items:
        obj["mediaTypes"] = []
        obj["formats"] = []
        if obj["record"]["value"] not in seen:
            unique_records.append(obj)
            seen.add(obj["record"]["value"])

        rec = [
            x for x in unique_records if x["record"]["value"] == obj["record"]["value"]
        ]
        if "mediaType" in obj and rec:
            rec[0]["mediaTypes"].append(obj["mediaType"]["value"])

        if "format" in obj and rec:
            rec[0]["formats"].append(obj["format"]["value"])

    return unique_records


def map_formats_to_prefixed(
    formats: List, media_types: dict, file_types: dict
) -> List[str]:
    formats_prefixed = []
    for fmt in formats:
        stripped_fmt = strip_http_scheme(fmt)
        if stripped_fmt in media_types:
            formats_prefixed.append("MEDIA_TYPE " + media_types[stripped_fmt].name)
        elif stripped_fmt in file_types:
            formats_prefixed.append("FILE_TYPE " + file_types[stripped_fmt].code)
        else:
            formats_prefixed.append("UNKNOWN")

    return formats_prefixed


def strip_http_scheme(uri: str) -> str:
    return uri.replace("https://", "").replace("http://", "")
