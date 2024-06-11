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
from fdk_reports_bff.service.referenced_data_store import get_los_path
from fdk_reports_bff.service.utils import ContentKeys, ServiceKey


def add_key_as_node_uri(key: str, value: dict) -> dict:
    value[EsMappings.NODE_URI] = key
    return value


async def add_formats_to_document(rdf_values: dict) -> dict:
    if EsMappings.MEDIATYPE in rdf_values.keys():
        rdf_values[EsMappings.MEDIATYPE][ContentKeys.VALUE] = [
            "https://www.iana.org/assignments/media-types/application/vnd.geo+json",
            "application/json",
        ]
    return rdf_values


def add_los_path_to_document(json_rdf_values: dict, los_themes: List[dict]) -> dict:
    if EsMappings.THEME in json_rdf_values.keys():
        themes = (
            json_rdf_values[EsMappings.THEME]
            if json_rdf_values.get(EsMappings.THEME)
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
        except Exception:
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


async def elasticsearch_get_dataset_catalog_titles(catalog_id: str) -> Any:
    query = {
        "query": {"match": {f"{EsMappings.PART_OF_CATALOG}.id.keyword": catalog_id}},
        "size": 1,
    }
    catalogs = es_client.search(index="datasets", body=query)["hits"]["hits"]
    return catalogs[0]["_source"]["partOfCatalog"].get("title")


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
            "_source": ["subject"],
            "size": 0,
            "query": {"exists": {"field": "subject"}},
            "aggregations": {
                "most_in_use": {
                    "terms": {
                        "field": "subject.keyword",
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
    unique_records: dict = dict()
    for obj in items:
        key = obj["record"]["value"]
        default_record: dict = {
            "mediaTypes": list(),
            "formats": list(),
            "themes": list(),
            "subjects": list(),
            "catalogTitles": dict(),
        }
        unique_record = unique_records.get(key, default_record)

        for field_key in obj:
            if field_key == "mediaType":
                unique_record["mediaTypes"].append(obj["mediaType"]["value"])
            if field_key == "format":
                unique_record["formats"].append(obj["format"]["value"])
            if field_key == "theme":
                unique_record["themes"].append(obj["theme"]["value"])
            if field_key == "subject":
                unique_record["subjects"].append(obj["subject"]["value"])
            elif field_key == "catalogTitle":
                catalog_titles = unique_record["catalogTitles"]
                lang_key = obj["catalogTitle"].get("xml:lang")
                lang_key = lang_key if lang_key is not None else "no"
                catalog_titles[lang_key] = obj["catalogTitle"].get("value")
                unique_record["catalogTitles"] = catalog_titles
            else:
                unique_record[field_key] = obj[field_key]
        unique_records[key] = unique_record

    return list(unique_records.values())


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
