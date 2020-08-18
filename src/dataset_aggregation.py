import asyncio

from src.organization_parser import OrganizationStore
from src.responses import DataSetResponse
from src.service_requests import get_datasets_statistics, get_datasets_access_rights, get_datasets_themes_and_topics, \
    fetch_datasets_catalog, get_datasets_formats
from src.sparql_utils.sparql_parsers import parse_sparql_formats_count, parse_sparql_access_rights_count, \
    parse_sparql_single_results, parse_sparql_catalogs_count, parse_sparql_themes_and_topics_count
from src.utils import ServiceKey, BadOrgPathException


def create_dataset_report(orgpath, theme):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    asyncio.set_event_loop(loop)
    organizations, simple_stats, access_rights, themes, dist_formats = loop.run_until_complete(
        gather_dataset_content_requests(orgpath, theme))
    parsing_tasks = asyncio.gather(
        parse_sparql_catalogs_count(organizations),
        parse_sparql_access_rights_count(access_rights),
        parse_sparql_themes_and_topics_count(themes)
    )
    catalogs, access_rights_count, themes_count = loop.run_until_complete(parsing_tasks)
    return DataSetResponse(
        themes=themes_count,
        catalogs=catalogs,
        single_aggregations=parse_sparql_single_results(simple_stats),
        access_rights=access_rights_count,
        dist_formats=parse_sparql_formats_count(dist_formats)
    )


def gather_dataset_content_requests(orgpath, theme):
    organization_uris = None
    theme = None
    if orgpath:
        try:
            organization_uris = OrganizationStore.get_instance().get_organization_uris_from_org_path(orgpath=orgpath)
        except BadOrgPathException:
            organization_uris = None

    return asyncio.gather(
        fetch_datasets_catalog(organization_uris, theme),
        get_datasets_statistics(organization_uris, theme),
        get_datasets_access_rights(organization_uris, theme),
        get_datasets_themes_and_topics(organization_uris, theme),
        get_datasets_formats(organization_uris, theme)
    )


report_functions = {
    ServiceKey.DATA_SETS: create_dataset_report
}
