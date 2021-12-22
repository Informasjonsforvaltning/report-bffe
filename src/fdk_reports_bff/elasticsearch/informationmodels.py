import asyncio
import logging
import traceback
from typing import List

from fdk_reports_bff.elasticsearch.queries import (
    EsMappings,
    INFORMATION_MODEL_AGGREGATION_FIELDS,
)
from fdk_reports_bff.elasticsearch.utils import (
    elasticsearch_ingest,
    get_unique_records,
)
from fdk_reports_bff.service.service_requests import get_informationmodels_statistic
from fdk_reports_bff.service.utils import FetchFromServiceException, ServiceKey


def insert_informationmodels(success_status: str, failed_status: str) -> str:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        model_tasks = asyncio.gather(get_informationmodels_statistic())
        info_models = loop.run_until_complete(model_tasks)[0]

        prepared_docs = loop.run_until_complete(
            prepare_documents(documents=info_models)
        )

        elasticsearch_ingest(ServiceKey.INFO_MODELS, prepared_docs)

        return success_status

    except FetchFromServiceException as err:
        logging.error(f"{traceback.format_exc()} {err.reason}")
        return failed_status


async def prepare_documents(documents: List[dict]) -> List[dict]:
    unique_record_items = get_unique_records(documents)
    return [
        reduce_informationmodel(informationmodel=informationmodel)
        for informationmodel in unique_record_items
    ]


def reduce_informationmodel(informationmodel: dict) -> dict:
    reduced_dict = informationmodel.copy()
    for items in informationmodel.items():
        key = items[0]
        if key not in INFORMATION_MODEL_AGGREGATION_FIELDS:
            reduced_dict.pop(key)
        elif key in EsMappings.ORG_PATH or key in EsMappings.ORGANIZATION_ID:
            reduced_dict[key] = informationmodel[key]["value"]
    return reduced_dict
