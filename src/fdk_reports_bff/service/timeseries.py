from typing import Any

from fdk_reports_bff.elasticsearch.queries import EsMappings
from fdk_reports_bff.elasticsearch.utils import elasticsearch_get_time_series
from fdk_reports_bff.responses import TimeSeriesResponse
from fdk_reports_bff.service.utils import QueryParameter, ServiceKey


def get_time_series(content_type: str, args: Any) -> TimeSeriesResponse:
    orgpath = args.get(QueryParameter.ORG_PATH)
    theme_profile = args.get(QueryParameter.THEME_PROFILE)
    organization_id = args.get(QueryParameter.ORGANIZATION_ID)
    if content_type == ServiceKey.DATA_SETS:
        return get_time_series_response(
            content_type=content_type,
            elastic_type=ServiceKey.DATASET_TIME_SERIES,
            org_path=orgpath,
            theme_profile=theme_profile,
            series_field=EsMappings.TIMESTAMP,
        )
    elif content_type == ServiceKey.CONCEPTS:
        return get_time_series_response(
            content_type=content_type,
            elastic_type=ServiceKey.CONCEPT_TIME_SERIES,
            org_path=orgpath,
            series_field=EsMappings.TIMESTAMP,
        )
    elif content_type in [
        ServiceKey.DATA_SERVICES,
        ServiceKey.INFO_MODELS,
    ]:
        return get_time_series_response(
            content_type=content_type,
            elastic_type=content_type,
            org_path=orgpath,
            organization_id=organization_id,
            series_field=f"{EsMappings.FIRST_HARVESTED}.value",
        )
    else:
        raise KeyError()


def get_time_series_response(
    content_type: str,
    elastic_type: str,
    org_path: Any = None,
    theme_profile: Any = None,
    organization_id: Any = None,
    series_field: Any = None,
) -> TimeSeriesResponse:
    es_time_series = elasticsearch_get_time_series(
        report_type=elastic_type,
        org_path=org_path,
        theme_profile=theme_profile,
        organization_id=organization_id,
        series_field=series_field,
    )
    return TimeSeriesResponse(es_time_series, content_type)
