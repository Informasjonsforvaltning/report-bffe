import asyncio

from src.elasticsearch.queries import EsMappings
from src.elasticsearch.utils import elasticsearch_get_concept_report_aggregations

from src.responses import ConceptResponse
from src.utils import ServiceKey, ContentKeys
from src.aggregation_utils import get_es_aggregation, get_es_cardinality_aggregation


def create_concept_report(orgpath, organization_id):
    es_report = elasticsearch_get_concept_report_aggregations(report_type=ServiceKey.CONCEPTS,
                                                              orgpath=orgpath,
                                                              organization_id=organization_id)

    return ConceptResponse(
        totalObjects=es_report[1]["hits"][ContentKeys.TOTAL][ContentKeys.VALUE],
        newLastWeek=get_es_aggregation(es_report[1], ContentKeys.NEW_LAST_WEEK),
        org_paths=get_es_aggregation(es_report[1], EsMappings.ORG_PATH),
        organizationCount=get_es_cardinality_aggregation(es_report[1], ContentKeys.ORGANIZATION_COUNT),
        most_in_use=get_es_aggregation(es_report[0], ContentKeys.MOST_IN_USE)
    )
