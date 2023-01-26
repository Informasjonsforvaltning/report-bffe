import asyncio
from datetime import datetime
import logging
import traceback
from typing import Any, Dict, List, Optional

from fdk_reports_bff.elasticsearch.queries import EsMappings
from fdk_reports_bff.elasticsearch.utils import (
    elasticsearch_ingest,
    first_of_month_timestamp_range,
    get_unique_records,
    map_formats_to_prefixed,
    strip_http_scheme,
)
from fdk_reports_bff.service.referenced_data_store import (
    get_file_types,
    get_los_path,
    get_media_types,
)
from fdk_reports_bff.service.service_requests import (
    fetch_dataset_time_series_datapoint,
    fetch_diff_store_metadata,
    fetch_themes_and_topics_from_reference_data,
    sparql_service_query,
)
from fdk_reports_bff.service.utils import (
    FetchFromServiceException,
    ServiceKey,
)
from fdk_reports_bff.sparql import (
    get_dataset_catalogs_query,
    get_dataset_distributions_query,
    get_dataset_publishers_query,
    get_datasets_query,
)


def insert_datasets(success_status: str, failed_status: str) -> str:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        collection_tasks = asyncio.gather(
            sparql_service_query(get_datasets_query()),
            sparql_service_query(get_dataset_catalogs_query()),
            sparql_service_query(get_dataset_distributions_query()),
            sparql_service_query(get_dataset_publishers_query()),
            fetch_themes_and_topics_from_reference_data(),
            get_media_types(),
            get_file_types(),
        )
        (
            datasets,
            dataset_catalogs,
            dataset_distributions,
            dataset_publishers,
            los_themes,
            media_types,
            file_types,
        ) = loop.run_until_complete(collection_tasks)
        prepared_docs = loop.run_until_complete(
            prepare_documents(
                datasets=datasets,
                dataset_catalogs=dataset_catalogs,
                dataset_distributions=dataset_distributions,
                dataset_publishers=dataset_publishers,
                los_themes=los_themes,
                media_types=media_types,
                file_types=file_types,
            )
        )
        elasticsearch_ingest(index_key=ServiceKey.DATA_SETS, documents=prepared_docs)
        return success_status
    except FetchFromServiceException as err:
        logging.error(f"{traceback.format_exc()} {err.reason}")
        return failed_status


def insert_datasets_timeseries(success_status: str, failed_status: str) -> str:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        diff_store_metadata = loop.run_until_complete(fetch_diff_store_metadata())
        if diff_store_is_empty(diff_store_metadata):
            return failed_status
        else:
            date_range = first_of_month_timestamp_range(
                start=diff_store_metadata.get("start_time"),
                end=diff_store_metadata.get("end_time"),
            )
            results = loop.run_until_complete(
                asyncio.gather(
                    *[
                        fetch_dataset_time_series_datapoint(timestamp)
                        for timestamp in date_range
                    ]
                )
            )
            prepared_docs = loop.run_until_complete(
                prepare_time_series(documents=results)
            )
            elasticsearch_ingest(
                index_key=ServiceKey.DATASET_TIME_SERIES, documents=prepared_docs
            )
            return success_status
    except FetchFromServiceException as err:
        logging.error(f"{traceback.format_exc()} {err.reason}")
        return failed_status


def diff_store_is_empty(diff_store_metadata: dict) -> bool:
    return diff_store_metadata.get("start_time") is None


async def prepare_documents(
    datasets: List[dict],
    dataset_catalogs: List[dict],
    dataset_distributions: List[dict],
    dataset_publishers: List[dict],
    los_themes: List[dict],
    media_types: List,
    file_types: List,
) -> list:
    all_dataset_data = list()
    all_dataset_data.extend(datasets)
    all_dataset_data.extend(dataset_catalogs)
    all_dataset_data.extend(dataset_distributions)
    all_dataset_data.extend(dataset_publishers)

    media_types_dict = {}
    for media_type in media_types:
        media_types_dict[strip_http_scheme(media_type.uri)] = media_type

    file_types_dict = {}
    for file_type in file_types:
        file_types_dict[strip_http_scheme(file_type.uri)] = file_type

    unique_datasets = get_unique_records(all_dataset_data)
    return [
        reduce_dataset(
            dataset=dataset,
            los_themes=los_themes,
            media_types=media_types_dict,
            file_types=file_types_dict,
        )
        for dataset in unique_datasets
    ]


async def prepare_time_series(
    documents: List[dict],
) -> list:
    datapoint_lists = [
        reduce_dataset_time_series(datapoint=datapoint) for datapoint in documents
    ]
    return [dataset for datapoint in datapoint_lists for dataset in datapoint]


def reduce_dataset_time_series(datapoint: dict) -> list:
    return [
        {
            "uri": str(dataset["dataset"]["value"]),
            "transportportal": bool(
                dataset.get("transportportal", {}).get("value", False)
            ),
            "orgPath": str(dataset.get("orgPath", {}).get("value", "MISSING")),
            "timestamp": datetime.fromtimestamp(int(datapoint["timestamp"])).strftime(
                "%Y-%m-%dT%H:%M:%S.00Z"
            ),
        }
        for dataset in datapoint["results"]
    ]


def reduce_dataset(
    dataset: dict,
    los_themes: List[dict],
    media_types: dict,
    file_types: dict,
) -> dict:
    catalog = {
        "id": string_value_from_sparql_result(dataset.get("catalog")),
        "title": dataset.get("catalogTitles"),
    }
    reduced_dict: Dict[str, Any] = {
        EsMappings.NODE_URI: string_value_from_sparql_result(dataset.get("dataset")),
        EsMappings.ORG_PATH: string_value_from_sparql_result(dataset.get("orgPath")),
        EsMappings.ORGANIZATION_ID: string_value_from_sparql_result(
            dataset.get("orgId")
        ),
        EsMappings.ACCESS_RIGHTS: (
            [dataset["accessRights"]] if dataset.get("accessRights") else None
        ),
        EsMappings.THEME: dataset["themes"],
        EsMappings.FORMAT: map_formats_to_prefixed(
            dataset["formats"] + dataset["mediaTypes"], media_types, file_types
        ),
        EsMappings.OPEN_LICENSE: bool_value_from_sparql_result(
            dataset.get("isOpenData")
        ),
        EsMappings.TRANSPORTPORTAL: bool_value_from_sparql_result(
            dataset.get("transportportal")
        ),
        EsMappings.PART_OF_CATALOG: catalog,
        EsMappings.PROVENANCE: dataset.get("provenance"),
        EsMappings.SUBJECT: dataset["subjects"],
        EsMappings.LOS: get_los_path(uri_list=dataset["themes"], los_themes=los_themes),
    }

    return reduced_dict


def string_value_from_sparql_result(obj: Optional[dict]) -> str:
    return obj["value"] if obj else None


def bool_value_from_sparql_result(obj: Optional[dict]) -> bool:
    return bool(obj["value"]) if obj else False
