from typing import List

from src.organization_parser import OrganizationStore, OrganizationReferencesObject
from asyncstdlib.functools import lru_cache as alru_cache
from src.service_requests import fetch_access_rights_from_reference_data, fetch_themes_and_topics_from_reference_data, \
    fetch_organization_from_catalog, fetch_organizations_from_organizations_catalog, \
    fetch_generated_org_path_from_organization_catalog, attempt_fetch_organization_by_name_from_catalog, \
    fetch_open_licences_from_reference_data, fetch_media_types_from_reference_data
from src.utils import NotInNationalRegistryException


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


class MediaTypes:

    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

    def __eq__(self, other):
        other_lower = other.lower()
        return other_lower in self.code.lower() or other_lower in self.name.lower()

    @staticmethod
    def from_reference_data_response(response: List[dict]):
        return [MediaTypes(name=entry.get("name"),
                           code=entry.get("code")) for entry in response]


@alru_cache
async def get_rights_statements() -> List[ParsedReferenceData]:
    rights_statements = await fetch_access_rights_from_reference_data()
    return ParsedReferenceData.from_rights_statement_list(rights_statements)


@alru_cache
async def get_los_paths() -> List[dict]:
    los_themes = await fetch_themes_and_topics_from_reference_data()
    return los_themes


@alru_cache
async def get_open_licenses() -> List[str]:
    open_licences = await fetch_open_licences_from_reference_data()
    licences: List[str] = [licence.get("uri") for licence in open_licences]
    http_safe_licences = licences.copy()
    for li in licences:
        if li.startswith("http://"):
            https_uri = "https://" + li.split("http://")[1]
            http_safe_licences.append(https_uri)
        elif li.startswith("https://"):
            http_uri = "http://" + li.split("https://")[1]
            http_safe_licences.append(http_uri)
    return http_safe_licences


@alru_cache
async def get_media_types() -> List[dict]:
    media_types = await fetch_media_types_from_reference_data()
    return MediaTypes.from_reference_data_response(media_types)


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
    if parsed_org is not None:
        OrganizationStore.get_instance().add_organization(parsed_org)
    return parsed_org


async def get_organization(organization: OrganizationReferencesObject) -> OrganizationReferencesObject:
    if organization is None:
        return None
    try:
        org_catalog = await get_organizations()
        org_idx = org_catalog.index(organization)
        organization: OrganizationReferencesObject = org_catalog[org_idx]
        if organization.org_path is None:
            return await get_organization_from_organization_catalog(uri=organization.org_uri, name=organization.name)
        else:
            return organization
    except ValueError:
        org: OrganizationReferencesObject = await get_organization_from_organization_catalog(uri=organization.org_uri,
                                                                                             name=organization.name)
        return org


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


def get_los_path(uri_list: List[str], los_themes: List[dict]) -> List[str]:
    uri_to_los_path_list = []
    for uri in uri_list:
        raw_uri = clean_uri(uri)
        try:
            theme_reference = [theme["losPaths"] for theme in los_themes if theme.get("uri") == raw_uri]
            if len(theme_reference) > 0:
                uri_to_los_path_list.extend(*theme_reference)
        except ValueError:
            continue
    return uri_to_los_path_list
