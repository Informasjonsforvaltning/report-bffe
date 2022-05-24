import asyncio
import logging
import traceback
from typing import Any, Dict, List, Optional

from fdk_reports_bff.elasticsearch.queries import EsMappings
from fdk_reports_bff.elasticsearch.utils import (
    elasticsearch_ingest,
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
    fetch_datasets,
    fetch_themes_and_topics_from_reference_data,
)
from fdk_reports_bff.service.utils import (
    FetchFromServiceException,
    ServiceKey,
)


def insert_datasets(success_status: str, failed_status: str) -> str:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        collection_tasks = asyncio.gather(
            fetch_datasets(),
            fetch_themes_and_topics_from_reference_data(),
            get_media_types(),
            get_file_types(),
        )
        (
            datasets,
            los_themes,
            media_types,
            file_types,
        ) = loop.run_until_complete(collection_tasks)
        prepared_docs = loop.run_until_complete(
            prepare_documents(
                documents=datasets,
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


async def prepare_documents(
    documents: List[dict],
    los_themes: List[dict],
    media_types: List,
    file_types: List,
) -> list:
    media_types_dict = {}
    for media_type in media_types:
        media_types_dict[strip_http_scheme(media_type.uri)] = media_type

    file_types_dict = {}
    for file_type in file_types:
        file_types_dict[strip_http_scheme(file_type.uri)] = file_type

    unique_datasets = get_unique_records(documents)
    return [
        reduce_dataset(
            dataset=dataset,
            los_themes=los_themes,
            media_types=media_types_dict,
            file_types=file_types_dict,
        )
        for dataset in unique_datasets
    ]


def reduce_dataset(
    dataset: dict,
    los_themes: List[dict],
    media_types: dict,
    file_types: dict,
) -> dict:
    reduced_dict: Dict[str, Any] = {
        EsMappings.NODE_URI: string_value_from_sparql_result(dataset.get("dataset")),
        EsMappings.ORG_PATH: string_value_from_sparql_result(dataset.get("orgPath")),
        EsMappings.ORGANIZATION_ID: string_value_from_sparql_result(
            dataset.get("orgId")
        ),
        EsMappings.ACCESS_RIGHTS: (
            [dataset["accessRights"]] if dataset.get("accessRights") else None
        ),
        EsMappings.TITLE: [
            dataset["titles"][title_key] for title_key in dataset["titles"]
        ],
        EsMappings.THEME: dataset["themes"],
        EsMappings.FORMAT: map_formats_to_prefixed(
            dataset["formats"] + dataset["mediaTypes"], media_types, file_types
        ),
        EsMappings.OPEN_LICENSE: bool_value_from_sparql_result(
            dataset.get("isOpenData")
        ),
        EsMappings.PART_OF_CATALOG: string_value_from_sparql_result(
            dataset.get("catalogTitle")
        ),
        EsMappings.FIRST_HARVESTED: dataset["firstHarvested"],
        EsMappings.PROVENANCE: dataset.get("provenance"),
        EsMappings.SUBJECT: dataset["subjects"],
        EsMappings.LOS: get_los_path(uri_list=dataset["themes"], los_themes=los_themes),
    }

    return reduced_dict


def string_value_from_sparql_result(obj: Optional[dict]) -> str:
    return obj["value"] if obj else None


def bool_value_from_sparql_result(obj: Optional[dict]) -> bool:
    return bool(obj["value"]) if obj else False
