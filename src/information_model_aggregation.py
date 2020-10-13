from src.aggregation_utils import get_es_aggregation, get_es_cardinality_aggregation
from src.elasticsearch.queries import EsMappings
from src.elasticsearch.utils import elasticsearch_get_report_aggregations
from src.responses import InformationModelResponse
from src.utils import ContentKeys, ServiceKey


def create_information_model_report(orgpath, organization_id):
    es_report = elasticsearch_get_report_aggregations(
        report_type=ServiceKey.INFO_MODELS,
        orgpath=orgpath,
        organization_id=organization_id,
    )

    return InformationModelResponse(
        total_objects=es_report["hits"][ContentKeys.TOTAL][ContentKeys.VALUE],
        new_last_week=get_es_aggregation(es_report, ContentKeys.NEW_LAST_WEEK),
        org_paths=get_es_aggregation(es_report, EsMappings.ORG_PATH),
        organization_count=get_es_cardinality_aggregation(
            es_report, ContentKeys.ORGANIZATION_COUNT
        ),
    )
