import asyncio
from functools import lru_cache
from typing import List

from src.organization_parser import ParsedOrganization
from src.service_requests import get_organizations_from_catalog, get_access_rights, get_themes_and_topics_from_service


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
            parsed_right = ParsedReferenceData.from_los_themes_and_topics_list(theme)
            los_list.append(parsed_right)
        return los_list


@lru_cache
def get_rights_statements() -> List[ParsedReferenceData]:
    loop = asyncio.get_event_loop()
    rights_statements = loop.run_until_complete(get_access_rights())
    return ParsedReferenceData.from_rights_statement_list(rights_statements)


@lru_cache
def get_los_paths() -> List[ParsedReferenceData]:
    loop = asyncio.get_event_loop()
    los_themes = loop.run_until_complete(get_themes_and_topics_from_service())
    return ParsedReferenceData.from_los_list(los_themes)


@lru_cache
def get_organizations() -> List[ParsedOrganization]:
    return get_organizations_from_catalog()


def get_organization_from_service(uri: str) -> ParsedOrganization:
    return None


@lru_cache()
def get_org_path(uri: str) -> str:
    raw_uri = clean_uri(uri)
    try:
        org_catalog = get_organizations()
        org_idx: ParsedOrganization = org_catalog.index(raw_uri)
        return org_catalog[org_idx].orgPath
    except ValueError:
        if ParsedOrganization.is_national_registry_uri(raw_uri):
            org: ParsedOrganization = get_organization_from_service(ParsedOrganization.resolve_id(uri=raw_uri))
            return org.orgPath
        else:
            return None


def clean_uri(uri_from_sparql: str):
    return uri_from_sparql.replace("<", "").replace(">", "")


def get_access_rights_code(uri: str) -> str:
    raw_uri = clean_uri(uri)
    access_rights = get_rights_statements()
    try:
        ar_idx = access_rights.index(raw_uri)
        return access_rights[ar_idx].ref_value
    except ValueError:
        return None


def get_los_path(uri: str) -> List[str]:
    raw_uri = clean_uri(uri)
    los_paths = get_los_paths()
    try:
        lp_idx = los_paths.index(raw_uri)
        return los_paths[lp_idx].ref_value
    except ValueError:
        return None
