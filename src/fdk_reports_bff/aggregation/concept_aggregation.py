from typing import Any

from fdk_reports_bff.aggregation.aggregation_utils import (
    get_es_aggregation,
    get_es_cardinality_aggregation,
)
from fdk_reports_bff.elasticsearch.queries import EsMappings
from fdk_reports_bff.elasticsearch.utils import (
    elasticsearch_get_concept_report_aggregations,
)
from fdk_reports_bff.responses import ConceptResponse
from fdk_reports_bff.service.utils import ContentKeys, ServiceKey


def create_concept_report(orgpath: Any, organization_id: Any) -> ConceptResponse:
    es_report = elasticsearch_get_concept_report_aggregations(
        report_type=ServiceKey.CONCEPTS,
        orgpath=orgpath,
        organization_id=organization_id,
    )

    return ConceptResponse(
        total_objects=es_report[1]["hits"][ContentKeys.TOTAL][ContentKeys.VALUE],
        new_last_week=get_es_aggregation(es_report[1], ContentKeys.NEW_LAST_WEEK),
        org_paths=get_es_aggregation(es_report[1], EsMappings.ORG_PATH),
        organization_count=get_es_cardinality_aggregation(
            es_report[1], ContentKeys.ORGANIZATION_COUNT
        ),
        most_in_use=get_es_aggregation(es_report[0], ContentKeys.MOST_IN_USE),
    )
