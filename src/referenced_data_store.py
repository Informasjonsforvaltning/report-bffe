from typing import List

from src.organization_parser import OrganizationStore, OrganizationReferencesObject
from asyncstdlib.functools import lru_cache as alru_cache
from src.service_requests import fetch_access_rights_from_reference_data, fetch_themes_and_topics_from_reference_data, \
    fetch_organization_from_catalog, fetch_organizations_from_organizations_catalog, \
    fetch_generated_org_path_from_organization_catalog, attempt_fetch_organization_by_name_from_catalog
from src.utils import NotInNationalRegistryException, ServiceKey


class ParsedReferenceData:
    def __init__(self, uri: str, reference: str = None):
        self.uri = uri
        self.ref_value = reference

    def __eq__(self, other):
        if type(other) is str:
            return self.uri == other
        elif type(other) == ParsedReferenceData:
            return self.uri == other.uri
        else:
            return False

    @staticmethod
    def from_rights_statement(json: dict):
        try:
            return ParsedReferenceData(uri=json["uri"], reference=json["code"])
        except KeyError:
            pass

    @staticmethod
    def from_rights_statement_list(reference_data_response: List[dict]):
        access_rights_list = []
        for rights_statement in reference_data_response:
            parsed_right = ParsedReferenceData.from_rights_statement(rights_statement)
            access_rights_list.append(parsed_right)
        return access_rights_list

    @staticmethod
    def from_los_themes_and_topics_list(json: dict):
        try:
            return ParsedReferenceData(uri=json["uri"], reference=json["losPaths"])
        except KeyError:
            pass

    @staticmethod
    def from_los_list(reference_data_response: List[dict]):
        los_list = []
        for theme in reference_data_response:
            parsed_theme = ParsedReferenceData.from_los_themes_and_topics_list(theme)
            los_list.append(parsed_theme)
        return los_list


@alru_cache
async def get_rights_statements() -> List[ParsedReferenceData]:
    rights_statements = await fetch_access_rights_from_reference_data()
    return ParsedReferenceData.from_rights_statement_list(rights_statements)


@alru_cache
async def get_los_paths() -> List[ParsedReferenceData]:
    los_themes = await fetch_themes_and_topics_from_reference_data()
    return ParsedReferenceData.from_los_list(los_themes)


@alru_cache
async def get_organizations() -> List[OrganizationReferencesObject]:
    organizations = await fetch_organizations_from_organizations_catalog()
    parsed_organizations = OrganizationReferencesObject.from_organization_catalog_list_response(organizations)
    org_store = OrganizationStore.get_instance()
    [org_store.add_organization(org) for org in parsed_organizations]
    return org_store.organizations


@alru_cache
async def get_organization_from_organization_catalog(uri: str, name: str) -> OrganizationReferencesObject:
    try:
        if OrganizationReferencesObject.is_national_registry_uri(uri):
            org = await fetch_organization_from_catalog(OrganizationReferencesObject.resolve_id(uri=uri), name)
        else:
            org = await attempt_fetch_organization_by_name_from_catalog(name)

        parsed_org = OrganizationReferencesObject.from_organization_catalog_single_response(org)

    except NotInNationalRegistryException:
        orgpath = await fetch_generated_org_path_from_organization_catalog(name)
        parsed_org = OrganizationReferencesObject(name=name, org_uri=uri, org_path=orgpath)

    OrganizationStore.get_instance().add_organization(parsed_org)
    return parsed_org


async def get_org_path(uri: str, name: str) -> str:
    raw_uri = clean_uri(uri)
    try:
        org_catalog = await get_organizations()
        org_idx: OrganizationReferencesObject = org_catalog.index(raw_uri)
        return org_catalog[org_idx].org_path
    except ValueError:
        org: OrganizationReferencesObject = await get_organization_from_organization_catalog(uri=raw_uri, name=name)
        return org.org_path


def clean_uri(uri_from_sparql: str):
    return uri_from_sparql.replace("<", "").replace(">", "")


async def get_access_rights_code(uri: str) -> str:
    raw_uri = clean_uri(uri)
    access_rights = await get_rights_statements()
    try:
        ar_idx = access_rights.index(raw_uri)
        return access_rights[ar_idx].ref_value
    except ValueError:
        return None


async def add_los_path_to_entry(entry: dict) -> dict:
    pass


async def get_los_path(uri: str) -> List[str]:
    raw_uri = clean_uri(uri)
    los_paths = await get_los_paths()
    try:
        lp_idx = los_paths.index(raw_uri)
        return los_paths[lp_idx].ref_value
    except ValueError:
        return []