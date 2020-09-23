from src.elasticsearch.queries import EsMappings
from src.elasticsearch.utils import elasticsearch_get_time_series
from src.rdf_namespaces import JSON_RDF
from src.responses import TimeSeriesResponse
from src.utils import ServiceKey, QueryParameter


def get_time_series(content_type: ServiceKey, args) -> TimeSeriesResponse:
    orgpath = args.get(QueryParameter.ORG_PATH)
    theme = args.get(QueryParameter.THEME)
    theme_profile = args.get(QueryParameter.THEME_PROFILE)
    organization_id = args.get(QueryParameter.ORGANIZATION_ID)
    if content_type == ServiceKey.DATA_SETS:
        return get_dataset_time_series(org_path=orgpath,
                                       theme=theme,
                                       theme_profile=theme_profile,
                                       organization_id=organization_id)
    elif content_type == ServiceKey.CONCEPTS:
        return get_concept_time_series(org_path=orgpath,
                                       organization_id=organization_id)
    else:
        raise KeyError()


def get_dataset_time_series(org_path=None, theme=None, theme_profile=None, organization_id=None) -> TimeSeriesResponse:
    es_time_series = elasticsearch_get_time_series(report_type=ServiceKey.DATA_SETS,
                                                   org_path=org_path,
                                                   theme=theme,
                                                   theme_profile=theme_profile,
                                                   organization_id=organization_id,
                                                   series_field=f"{EsMappings.RECORD}.{JSON_RDF.dct.issued}.value")
    return TimeSeriesResponse(es_time_series)


def get_concept_time_series(org_path=None, organization_id=None) -> TimeSeriesResponse:
    es_time_series = elasticsearch_get_time_series(report_type=ServiceKey.CONCEPTS,
                                                   org_path=org_path,
                                                   organization_id=organization_id,
                                                   series_field=EsMappings.FIRST_HARVESTED)
    return TimeSeriesResponse(es_time_series)
