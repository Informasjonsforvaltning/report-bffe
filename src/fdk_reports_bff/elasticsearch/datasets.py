import asyncio
import logging
import traceback
from typing import List

from fdk_reports_bff.elasticsearch.queries import DATASET_AGGREGATION_FIELDS, EsMappings
from fdk_reports_bff.elasticsearch.rdf_reference_mappers import RdfReferenceMapper
from fdk_reports_bff.elasticsearch.utils import (
    add_key_as_node_uri,
    add_org_and_los_paths_to_document,
    elasticsearch_ingest,
    get_all_organizations_with_publisher,
)
from fdk_reports_bff.service.rdf_namespaces import JsonRDF
from fdk_reports_bff.service.referenced_data_store import (
    get_media_types,
    get_open_licenses,
)
from fdk_reports_bff.service.service_requests import (
    fetch_catalog_from_dataset_harvester,
    fetch_publishers_from_dataset_harvester,
    fetch_themes_and_topics_from_reference_data,
)
from fdk_reports_bff.service.utils import (
    ContentKeys,
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
            fetch_catalog_from_dataset_harvester(),
            fetch_themes_and_topics_from_reference_data(),
            get_open_licenses(),
            get_media_types(),
            fetch_publishers_from_dataset_harvester(),
        )
        (
            dataset_rdf,
            los_themes,
            open_licenses,
            media_types,
            publishers,
        ) = loop.run_until_complete(collection_tasks)
        prepared_docs = loop.run_until_complete(
            prepare_documents(
                documents=dataset_rdf,
                los_themes=los_themes,
                open_licenses=open_licenses,
                media_types=media_types,
                publishers=publishers,
            )
        )
        elasticsearch_ingest(index_key=ServiceKey.DATA_SETS, documents=prepared_docs)
        return success_status
    except FetchFromServiceException as err:
        logging.error(f"{traceback.format_exc()} {err.reason}")
        return failed_status


async def prepare_documents(
    documents: dict,
    los_themes: List[dict],
    open_licenses: List[str],
    media_types: List[dict],
    publishers: dict,
) -> list:
    await get_all_organizations_with_publisher(publishers)

    documents_list = list(documents.items())
    dicts_with_mapped_node_uri = [
        add_key_as_node_uri(value=entry[1], key=entry[0]) for entry in documents_list
    ]
    datasets = [
        entry
        for entry in dicts_with_mapped_node_uri
        if JsonRDF.rdf_type_equals(JsonRDF.dcat.type_dataset, entry)
    ]
    reference_mapper = RdfReferenceMapper(
        document_list=documents_list,
        open_licenses=open_licenses,
        media_types=media_types,
    )
    datasets_with_fdk_portal_paths = await asyncio.gather(
        *[
            add_org_and_los_paths_to_document(
                json_rdf_values=entry, los_themes=los_themes
            )
            for entry in datasets
        ]
    )

    return [
        merge_dataset_information(dataset=dataset, reference_mapper=reference_mapper)
        for dataset in datasets_with_fdk_portal_paths
    ]


def merge_dataset_information(
    dataset: dict, reference_mapper: RdfReferenceMapper
) -> dict:
    dataset_record = reference_mapper.get_catalog_record_for_dataset(
        dataset[EsMappings.NODE_URI]
    )
    if dataset_record is not None:
        dataset[EsMappings.RECORD] = dataset_record
        is_part_of = (
            dataset_record[JsonRDF.dct.isPartOf]
            if dataset_record.get(JsonRDF.dct.isPartOf)
            else []
        )
        dataset[EsMappings.PART_OF_CATALOG] = reference_mapper.get_dataset_catalog_name(
            record_part_of_uri=is_part_of[0].get(ContentKeys.VALUE)
            if len(is_part_of) > 0
            else None,
            dataset_node_uri=dataset[EsMappings.NODE_URI],
        )
    if dataset.get(JsonRDF.dcat.distribution):
        dataset[
            JsonRDF.dcat.distribution
        ] = reference_mapper.get_distributions_in_entry(
            entry=dataset, node_uri=dataset[EsMappings.NODE_URI]
        )
        dataset[EsMappings.OPEN_LICENSE] = reference_mapper.has_open_license(
            dcat_distributions=dataset[JsonRDF.dcat.distribution]
        )

        dataset[EsMappings.FORMAT] = reference_mapper.get_formats_with_codes(
            dcat_distributions=dataset[JsonRDF.dcat.distribution]
        )
    return reduce_dataset(dataset)


def reduce_dataset(dataset: dict) -> dict:
    reduced_dict = dataset.copy()
    for items in dataset.items():
        key = items[0]
        if key not in DATASET_AGGREGATION_FIELDS:
            reduced_dict.pop(key)
    return reduced_dict
