import asyncio

from src.elasticsearch.queries import EsMappings
from src.elasticsearch.utils import elasticsearch_get_report_aggregations

from src.responses import DataServiceResponse
from src.utils import ServiceKey, ContentKeys
from src.aggregation_utils import get_es_aggregation, get_es_cardinality_aggregation


def create_dataservice_report(orgpath, organization_id):
    es_report = elasticsearch_get_report_aggregations(report_type=ServiceKey.DATA_SERVICES,
                                                      orgpath=orgpath,
                                                      organization_id=organization_id)

    return DataServiceResponse(
        totalObjects=es_report["hits"][ContentKeys.TOTAL][ContentKeys.VALUE],
        newLastWeek=get_es_aggregation(es_report, ContentKeys.NEW_LAST_WEEK),
        org_paths=get_es_aggregation(es_report, EsMappings.ORG_PATH),
        organizationCount=get_es_cardinality_aggregation(es_report, ContentKeys.ORGANIZATION_COUNT),
        mediaTypes = get_es_aggregation(es_report, ContentKeys.MEDIATYPE)
    )
