from fdk_reports_bff.elasticsearch.queries import EsMappings
from fdk_reports_bff.elasticsearch.utils import elasticsearch_get_time_series
from fdk_reports_bff.rdf_namespaces import JsonRDF
from fdk_reports_bff.responses import TimeSeriesResponse
from fdk_reports_bff.utils import QueryParameter, ServiceKey


def get_time_series(content_type: ServiceKey, args: any) -> TimeSeriesResponse:
    orgpath = args.get(QueryParameter.ORG_PATH)
    theme = args.get(QueryParameter.THEME)
    theme_profile = args.get(QueryParameter.THEME_PROFILE)
    organization_id = args.get(QueryParameter.ORGANIZATION_ID)
    if content_type == ServiceKey.DATA_SETS:
        return get_time_series_response(
            report_type=content_type,
            org_path=orgpath,
            theme=theme,
            theme_profile=theme_profile,
            organization_id=organization_id,
            series_field=f"{EsMappings.RECORD}.{JsonRDF.dct.issued}.value",
        )
    elif content_type == ServiceKey.DATA_SERVICES:
        return get_time_series_response(
            report_type=content_type,
            org_path=orgpath,
            organization_id=organization_id,
            series_field=f"{EsMappings.ISSUED}.value",
        )
    elif content_type in [ServiceKey.CONCEPTS, ServiceKey.INFO_MODELS]:
        return get_time_series_response(
            report_type=content_type,
            org_path=orgpath,
            organization_id=organization_id,
            series_field=f"{EsMappings.ISSUED}.value",
        )
    else:
        raise KeyError()


def get_time_series_response(
    report_type: any = None,
    org_path: any = None,
    theme: any = None,
    theme_profile: any = None,
    organization_id: any = None,
    series_field: any = None,
) -> TimeSeriesResponse:
    es_time_series = elasticsearch_get_time_series(
        report_type=report_type,
        org_path=org_path,
        theme=theme,
        theme_profile=theme_profile,
        organization_id=organization_id,
        series_field=series_field,
    )
    return TimeSeriesResponse(es_time_series)
