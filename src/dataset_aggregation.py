from src.elasticsearch.queries import EsMappings
from src.elasticsearch.utils import elasticsearch_get_report_aggregations
from src.rdf_namespaces import ContentKeys
from src.responses import DataSetResponse
from src.utils import ServiceKey


def create_dataset_report(orgpath, theme, theme_profile):
    es_report = elasticsearch_get_report_aggregations(report_type=ServiceKey.DATA_SETS,
                                                      orgpath=orgpath,
                                                      theme=theme,
                                                      theme_profile=theme_profile)

    return DataSetResponse(
        total=es_report["hits"][ContentKeys.TOTAL][ContentKeys.VALUE],
        new_last_week=get_es_aggregation(es_report, ContentKeys.NEW_LAST_WEEK),
        dist_formats=get_es_aggregation(es_report, ContentKeys.FORMAT),
        opendata=get_es_aggregation(es_report, ContentKeys.OPEN_DATA),
        national_component=get_es_aggregation(es_report, ContentKeys.NATIONAL_COMPONENT),
        catalogs=get_es_aggregation(es_report, EsMappings.ORG_PATH),
        themes=get_es_aggregation(es_report, ContentKeys.LOS_PATH),
        with_subject=get_es_aggregation(es_report, ContentKeys.WITH_SUBJECT),
        access_rights=get_es_aggregation(es_report, ContentKeys.ACCESS_RIGHTS_CODE)

    )


def get_es_aggregation(es_hits: dict, content_key):
    single_aggregations = [ContentKeys.NEW_LAST_WEEK,
                           ContentKeys.NATIONAL_COMPONENT,
                           ContentKeys.OPEN_DATA,
                           ContentKeys.WITH_SUBJECT,
                           ]
    if content_key in single_aggregations:
        return es_hits.get("aggregations").get(content_key)["doc_count"]
    else:
        buckets = es_hits.get("aggregations").get(content_key)["buckets"]
        return rename_doc_count_to_count(buckets)


def rename_doc_count_to_count(aggregation_buckets):
    return [{"key": bucket["key"], "count": bucket["doc_count"]} for bucket in aggregation_buckets]
