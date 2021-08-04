from typing import Any

from fdk_reports_bff.concept_aggregation import create_concept_report
from fdk_reports_bff.dataservice_aggregation import create_dataservice_report
from fdk_reports_bff.dataset_aggregation import create_dataset_report
from fdk_reports_bff.information_model_aggregation import (
    create_information_model_report,
)
from fdk_reports_bff.utils import QueryParameter, ServiceKey


def get_report(content_type: str, args: dict) -> Any:
    orgpath = args.get(QueryParameter.ORG_PATH)
    theme = args.get(QueryParameter.THEME)
    theme_profile = args.get(QueryParameter.THEME_PROFILE)
    organization_id = args.get(QueryParameter.ORGANIZATION_ID)
    if content_type == ServiceKey.DATA_SETS:
        return create_dataset_report(orgpath, theme, theme_profile, organization_id)
    elif content_type == ServiceKey.CONCEPTS:
        return create_concept_report(orgpath, organization_id)
    elif content_type == ServiceKey.INFO_MODELS:
        return create_information_model_report(orgpath, organization_id)
    elif content_type == ServiceKey.DATA_SERVICES:
        return create_dataservice_report(orgpath, organization_id)
    else:
        raise KeyError()
