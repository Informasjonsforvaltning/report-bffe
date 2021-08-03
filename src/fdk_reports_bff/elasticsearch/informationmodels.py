import asyncio
import logging

from fdk_reports_bff.elasticsearch.queries import EsMappings, INFORMATION_MODEL_AGGREGATION_FIELDS
from fdk_reports_bff.organization_parser import OrganizationReferencesObject
from fdk_reports_bff.utils import FetchFromServiceException


def insert_informationmodels(success_status, failed_status):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    try:
        # informationmodels = loop.run_until_complete(get_informationmodels_statistic())
        #
        # informationmodels = [
        #     add_es_aggregation_fields(informationmodel=informationmodel)
        #     for informationmodel in informationmodels
        # ]
        #
        # elasticsearch_ingest(ServiceKey.INFO_MODELS, informationmodels)
        return success_status

    except FetchFromServiceException as err:
        logging.error(err.reason)
        return failed_status


def add_es_aggregation_fields(informationmodel) -> dict:
    if informationmodel.get(EsMappings.PUBLISHER):
        informationmodel[EsMappings.ORG_PATH] = informationmodel[EsMappings.PUBLISHER][
            EsMappings.ORG_PATH
        ]
        informationmodel[
            EsMappings.ORGANIZATION_ID
        ] = OrganizationReferencesObject.resolve_id(
            informationmodel[EsMappings.PUBLISHER][EsMappings.URI]
        )
    return reduce_informationmodel(informationmodel=informationmodel)


def reduce_informationmodel(informationmodel: dict):
    reduced_dict = informationmodel.copy()
    for items in informationmodel.items():
        key = items[0]
        if key not in INFORMATION_MODEL_AGGREGATION_FIELDS:
            reduced_dict.pop(key)
    return reduced_dict
