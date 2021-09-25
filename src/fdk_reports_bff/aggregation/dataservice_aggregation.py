from typing import Any

from fdk_reports_bff.aggregation.aggregation_utils import (
    get_es_aggregation,
    get_es_cardinality_aggregation,
)
from fdk_reports_bff.elasticsearch.queries import EsMappings
from fdk_reports_bff.elasticsearch.utils import elasticsearch_get_report_aggregations
from fdk_reports_bff.responses import DataServiceResponse
from fdk_reports_bff.service.utils import ContentKeys, ServiceKey


def create_dataservice_report(orgpath: Any, organization_id: Any) -> Any:
    es_report = elasticsearch_get_report_aggregations(
        report_type=ServiceKey.DATA_SERVICES,
        orgpath=orgpath,
        organization_id=organization_id,
    )

    return DataServiceResponse(
        total_objects=es_report["hits"][ContentKeys.TOTAL][ContentKeys.VALUE],
        new_last_week=get_es_aggregation(es_report, ContentKeys.NEW_LAST_WEEK),
        org_paths=get_es_aggregation(es_report, EsMappings.ORG_PATH),
        organization_count=get_es_cardinality_aggregation(
            es_report, ContentKeys.ORGANIZATION_COUNT
        ),
        formats=get_es_aggregation(es_report, ContentKeys.FORMAT),
    )
