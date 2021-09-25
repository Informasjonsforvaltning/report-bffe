import asyncio
import logging
import traceback
from typing import List

from fdk_reports_bff.elasticsearch.queries import (
    DATASERVICE_AGGREGATION_FIELDS,
    EsMappings,
)
from fdk_reports_bff.elasticsearch.utils import (
    add_org_paths_to_document,
    elasticsearch_ingest,
    get_all_organizations_with_publisher,
    get_unique_records,
    map_formats_to_prefixed,
    strip_http_scheme,
)
from fdk_reports_bff.service.referenced_data_store import (
    FileTypes,
    get_file_types,
    get_media_types,
    MediaTypes,
)
from fdk_reports_bff.service.service_requests import (
    fetch_dataservices,
    fetch_publishers_from_dataservice,
)
from fdk_reports_bff.service.utils import FetchFromServiceException, ServiceKey


def insert_dataservices(success_status: str, failed_status: str) -> str:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        collection_tasks = asyncio.gather(
            fetch_dataservices(),
            fetch_publishers_from_dataservice(),
            get_media_types(),
            get_file_types(),
        )
        dataservices, publishers, media_types, file_types = loop.run_until_complete(
            collection_tasks
        )
        prepared_docs = loop.run_until_complete(
            prepare_documents(
                documents=dataservices,
                publishers=publishers,
                media_types=media_types,
                file_types=file_types,
            )
        )
        elasticsearch_ingest(
            index_key=ServiceKey.DATA_SERVICES, documents=prepared_docs
        )
        return success_status
    except FetchFromServiceException as err:
        logging.error(f"{traceback.format_exc()} {err.reason}")
        return failed_status


async def prepare_documents(
    documents: List[dict],
    publishers: dict,
    media_types: List[MediaTypes],
    file_types: List[FileTypes],
) -> List[dict]:
    await get_all_organizations_with_publisher(publishers)
    dataservices_with_fdk_portal_paths = await asyncio.gather(
        *[add_org_paths_to_document(rdf_values=entry) for entry in documents]
    )

    unique_record_items = get_unique_records(dataservices_with_fdk_portal_paths)

    media_types_dict = {}
    for media_type in media_types:
        media_types_dict[strip_http_scheme(media_type.uri)] = media_type

    file_types_dict = {}
    for file_type in file_types:
        file_types_dict[strip_http_scheme(file_type.uri)] = file_type

    for document in documents:
        document[EsMappings.FORMAT] = get_prefixed_formats_for_dataservice(
            dataservice=document,
            media_types=media_types_dict,
            file_types=file_types_dict,
        )

    return [
        reduce_dataservice(dataservice=dataservice)
        for dataservice in unique_record_items
    ]


def get_prefixed_formats_for_dataservice(
    dataservice: dict, media_types: dict, file_types: dict
) -> List[str]:
    format_str_values = []
    if "formats" in dataservice:
        for format in dataservice["formats"]:
            format_str_values.append(format)

    if "mediaTypes" in dataservice:
        for format in dataservice["mediaTypes"]:
            format_str_values.append(format)

    return map_formats_to_prefixed(
        list(set(format_str_values)), media_types, file_types
    )


def reduce_dataservice(dataservice: dict) -> dict:
    reduced_dict = dataservice.copy()
    for items in dataservice.items():
        key = items[0]
        if key not in DATASERVICE_AGGREGATION_FIELDS:
            reduced_dict.pop(key)
    return reduced_dict
