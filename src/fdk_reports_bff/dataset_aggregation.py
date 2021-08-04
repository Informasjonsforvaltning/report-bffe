import asyncio

from fdk_reports_bff.aggregation_utils import (
    get_es_aggregation,
    get_es_cardinality_aggregation,
)
from fdk_reports_bff.elasticsearch.queries import EsMappings
from fdk_reports_bff.elasticsearch.utils import elasticsearch_get_report_aggregations
from fdk_reports_bff.referenced_data_store import get_access_rights_code
from fdk_reports_bff.responses import DataSetResponse
from fdk_reports_bff.utils import ContentKeys, ServiceKey


def create_dataset_report(orgpath, theme, theme_profile, organization_id):
    es_report = elasticsearch_get_report_aggregations(
        report_type=ServiceKey.DATA_SETS,
        orgpath=orgpath,
        theme=theme,
        theme_profile=theme_profile,
        organization_id=organization_id,
    )

    rdf_access_rights_bucket = get_es_aggregation(
        es_report, ContentKeys.ACCESS_RIGHTS_CODE
    )
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    access_right_code_tasks = asyncio.gather(
        *[
            map_access_rights_to_code(access_right)
            for access_right in rdf_access_rights_bucket
        ]
    )
    mapped_access_rights = loop.run_until_complete(access_right_code_tasks)

    return DataSetResponse(
        total=es_report["hits"][ContentKeys.TOTAL][ContentKeys.VALUE],
        new_last_week=get_es_aggregation(es_report, ContentKeys.NEW_LAST_WEEK),
        dist_formats=get_es_aggregation(es_report, ContentKeys.FORMAT),
        opendata=get_es_aggregation(es_report, ContentKeys.OPEN_DATA),
        national_component=get_es_aggregation(
            es_report, ContentKeys.NATIONAL_COMPONENT
        ),
        org_paths=get_es_aggregation(es_report, EsMappings.ORG_PATH),
        themes=get_es_aggregation(es_report, ContentKeys.LOS_PATH),
        with_subject=get_es_aggregation(es_report, ContentKeys.WITH_SUBJECT),
        access_rights=mapped_access_rights,
        catalogs=get_es_aggregation(es_report, ContentKeys.CATALOGS),
        theme_profile=theme_profile,
        organization_count=get_es_cardinality_aggregation(
            es_report, ContentKeys.ORGANIZATION_COUNT
        ),
    )


async def map_access_rights_to_code(access_right: dict):
    rdf_key = access_right[ContentKeys.KEY]
    if rdf_key == EsMappings.MISSING:
        code_key = EsMappings.MISSING
    else:
        code_key = await get_access_rights_code(rdf_key)
    return {
        ContentKeys.KEY: code_key,
        ContentKeys.COUNT: access_right[ContentKeys.COUNT],
    }
