from typing import Any

from fdk_reports_bff.elasticsearch.queries import EsMappings
from fdk_reports_bff.service.utils import ContentKeys


def get_es_aggregation(es_hits: dict, content_key: str) -> Any:
    single_aggregations = [
        ContentKeys.NEW_LAST_WEEK,
        ContentKeys.NATIONAL_COMPONENT,
        ContentKeys.OPEN_DATA,
        ContentKeys.WITH_SUBJECT,
    ]
    if content_key in single_aggregations:
        return es_hits[EsMappings.AGGREGATIONS][content_key][EsMappings.DOC_COUNT]
    else:
        buckets = es_hits[EsMappings.AGGREGATIONS][content_key][EsMappings.BUCKETS]
        return rename_doc_count_to_count(buckets)


def get_es_cardinality_aggregation(es_hits: dict, content_key: str) -> Any:
    return es_hits[EsMappings.AGGREGATIONS][content_key][ContentKeys.VALUE]


def rename_doc_count_to_count(aggregation_buckets: Any) -> list:
    return [
        {
            ContentKeys.KEY: bucket[ContentKeys.KEY],
            ContentKeys.COUNT: bucket[EsMappings.DOC_COUNT],
        }
        for bucket in aggregation_buckets
    ]
