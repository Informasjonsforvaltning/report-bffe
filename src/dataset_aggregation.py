import asyncio

from src.organization_parser import OrganizationStore
from src.responses import DataSetResponse
from src.service_requests import query_simple_statistic, get_datasets_access_rights, get_datasets_themes_and_topics, \
    fetch_datasets_catalog, get_datasets_formats
from src.sparql_utils import ContentKeys
from src.sparql_utils.sparql_parsers import parse_sparql_formats_count, parse_sparql_access_rights_count, \
    parse_sparql_catalogs_count, parse_sparql_themes_and_topics_count, \
    parse_sparql_single_statistic
from src.utils import ServiceKey, BadOrgPathException


def create_dataset_report(orgpath, theme, theme_profile):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    asyncio.set_event_loop(loop)
    organizations, access_rights, themes, dist_formats, total, with_subject, new_last_week, opendata, national_component = loop.run_until_complete(
        gather_dataset_content_requests(orgpath, theme, theme_profile))
    parsing_tasks = asyncio.gather(
        parse_sparql_catalogs_count(organizations),
        parse_sparql_access_rights_count(access_rights),
        parse_sparql_themes_and_topics_count(themes)
    )
    catalogs, access_rights_count, themes_count = loop.run_until_complete(
        parsing_tasks)
    return DataSetResponse(
        themes=themes_count,
        catalogs=catalogs,
        access_rights=access_rights_count,
        dist_formats=parse_sparql_formats_count(dist_formats),
        total=parse_sparql_single_statistic(ContentKeys.TOTAL, total),
        with_subject=parse_sparql_single_statistic(ContentKeys.WITH_SUBJECT, with_subject),
        new_last_week=parse_sparql_single_statistic(ContentKeys.NEW_LAST_WEEK, new_last_week),
        opendata=parse_sparql_single_statistic(ContentKeys.OPEN_DATA, opendata),
        national_component=parse_sparql_single_statistic(ContentKeys.NATIONAL_COMPONENT,
                                                         national_component)
    )


def gather_dataset_content_requests(orgpath, theme, theme_profile):
    organization_uris = None
    theme = None
    if orgpath:
        try:
            organization_uris = OrganizationStore.get_instance().get_dataset_reference_for_orgpath(orgpath=orgpath)
        except BadOrgPathException:
            organization_uris = None

    return asyncio.gather(
        fetch_datasets_catalog(org_uris=organization_uris, theme=theme, theme_profile=theme_profile),
        get_datasets_access_rights(organization_uris, theme, theme_profile),
        get_datasets_themes_and_topics(organization_uris, theme),
        get_datasets_formats(organization_uris, theme, theme_profile),
        query_simple_statistic(field=ContentKeys.TOTAL, org_uris=organization_uris, theme=theme),
        query_simple_statistic(field=ContentKeys.WITH_SUBJECT, org_uris=organization_uris, theme=theme),
        query_simple_statistic(field=ContentKeys.NEW_LAST_WEEK, org_uris=organization_uris, theme=theme),
        query_simple_statistic(field=ContentKeys.OPEN_DATA, org_uris=organization_uris, theme=theme),
        query_simple_statistic(field=ContentKeys.NATIONAL_COMPONENT, org_uris=organization_uris, theme=theme),

    )


report_functions = {
    ServiceKey.DATA_SETS: create_dataset_report
}
