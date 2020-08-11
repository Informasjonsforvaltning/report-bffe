import asyncio

from src.responses import DataSetResponse
from src.service_requests import get_datasets_statistics, get_datasets_access_rights, get_datasets_themes_and_topics, \
    get_datasets_catalog, get_datasets_formats
from src.sparql_utils.sparql_parsers import parse_sparql_formats_count, parse_sparql_access_rights_count, \
    parse_sparql_single_results, parse_sparql_catalogs_count, parse_sparql_themes_and_topics_count
from src.utils import ServiceKey


def get_report(content_type: ServiceKey):
    return report_functions[content_type]()


def create_dataset_report():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    asyncio.set_event_loop(loop)
    dataset_content_requests = asyncio.gather(
        get_datasets_catalog(),
        get_datasets_statistics(),
        get_datasets_access_rights(),
        get_datasets_themes_and_topics(),
        get_datasets_formats()
    )
    organizations, simple_stats, access_rights, themes, dist_formats = loop.run_until_complete(dataset_content_requests)
    parsing_tasks = asyncio.gather(
        parse_sparql_catalogs_count(organizations),
        parse_sparql_access_rights_count(access_rights)
    )
    catalogs, access_rights_count = loop.run_until_complete(parsing_tasks)
    return DataSetResponse(
        themes=parse_sparql_themes_and_topics_count,
        catalogs=catalogs,
        single_aggregations=parse_sparql_single_results(simple_stats),
        access_rights=access_rights_count,
        dist_formats=parse_sparql_formats_count(dist_formats)
    )


report_functions = {
    ServiceKey.DATA_SETS: create_dataset_report
}
