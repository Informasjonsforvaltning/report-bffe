import asyncio
import logging
import traceback
from typing import List

from fdk_reports_bff.elasticsearch.queries import INFORMATION_MODEL_AGGREGATION_FIELDS
from fdk_reports_bff.elasticsearch.utils import (
    add_org_paths_to_document,
    elasticsearch_ingest,
    get_all_organizations_with_publisher,
    get_unique_records,
)
from fdk_reports_bff.service_requests import (
    fetch_info_model_publishers,
    get_informationmodels_statistic,
)
from fdk_reports_bff.utils import FetchFromServiceException, ServiceKey


def insert_informationmodels(success_status: str, failed_status: str) -> str:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        model_tasks = asyncio.gather(
            get_informationmodels_statistic(), fetch_info_model_publishers()
        )
        info_models, publishers = loop.run_until_complete(model_tasks)

        prepared_docs = loop.run_until_complete(
            prepare_documents(documents=info_models, publishers=publishers)
        )

        elasticsearch_ingest(ServiceKey.INFO_MODELS, prepared_docs)

        return success_status

    except FetchFromServiceException as err:
        logging.error(f"{traceback.format_exc()} {err.reason}")
        return failed_status


async def prepare_documents(documents: dict, publishers: dict) -> List[dict]:
    unique_record_items = get_unique_records(documents)

    await get_all_organizations_with_publisher(publishers)
    models_with_fdk_portal_paths = await asyncio.gather(
        *[add_org_paths_to_document(rdf_values=entry) for entry in unique_record_items]
    )

    return [
        reduce_informationmodel(informationmodel=informationmodel)
        for informationmodel in models_with_fdk_portal_paths
    ]


def reduce_informationmodel(informationmodel: dict) -> dict:
    reduced_dict = informationmodel.copy()
    for items in informationmodel.items():
        key = items[0]
        if key not in INFORMATION_MODEL_AGGREGATION_FIELDS:
            reduced_dict.pop(key)
    return reduced_dict
