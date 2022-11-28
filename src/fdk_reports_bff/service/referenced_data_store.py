from typing import Any, List, Optional

from asyncstdlib.functools import lru_cache as alru_cache

from fdk_reports_bff.service.service_requests import (
    fetch_access_rights_from_reference_data,
    fetch_file_types_from_reference_data,
    fetch_media_types_from_reference_data,
    fetch_themes_and_topics_from_reference_data,
)


class ParsedReferenceData:
    def __init__(self: Any, uri: str, reference: Optional[str] = None) -> None:
        self.uri = uri
        self.ref_value = reference

    def __eq__(self: Any, other: Any) -> bool:
        if type(other) is str:
            return self.uri == other
        elif type(other) == ParsedReferenceData:
            return self.uri == other.uri
        else:
            return False

    @staticmethod
    def from_rights_statement(json: dict) -> Any:
        try:
            return ParsedReferenceData(uri=json["uri"], reference=json["code"])
        except KeyError:
            pass

    @staticmethod
    def from_rights_statement_list(reference_data_response: List[dict]) -> List:
        access_rights_list = []
        for rights_statement in reference_data_response:
            parsed_right = ParsedReferenceData.from_rights_statement(rights_statement)
            access_rights_list.append(parsed_right)
        return access_rights_list

    @staticmethod
    def from_los_themes_and_topics_list(json: dict) -> Any:
        try:
            return ParsedReferenceData(uri=json["uri"], reference=json["losPaths"])
        except KeyError:
            pass

    @staticmethod
    def from_los_list(reference_data_response: List[dict]) -> List:
        los_list = []
        for theme in reference_data_response:
            parsed_theme = ParsedReferenceData.from_los_themes_and_topics_list(theme)
            los_list.append(parsed_theme)
        return los_list


class MediaTypes:
    def __init__(
        self: Any, uri: Optional[str], name: Optional[str], code: Optional[str]
    ) -> None:
        self.uri = uri
        self.name = name
        self.code = code

    def __eq__(self: Any, other: Any) -> bool:
        other_lower = other.lower()
        return other_lower in self.uri.lower() or other_lower in self.code.lower()

    @staticmethod
    def from_reference_data_response(response: List[dict]) -> List:
        return [
            MediaTypes(
                uri=entry.get("uri", ""),
                name=entry.get("name", ""),
                code=entry.get("type", "") + "/" + entry.get("subType", ""),
            )
            for entry in response
        ]


class FileTypes:
    def __init__(self: Any, uri: Optional[str], code: Optional[str]) -> None:
        self.uri = uri
        self.code = code

    def __eq__(self: Any, other: Any) -> bool:
        other_lower = other.lower()
        return other_lower in self.uri.lower() or other_lower in self.code.lower()

    @staticmethod
    def from_reference_data_response(response: List[dict]) -> List:
        return [
            FileTypes(uri=entry.get("uri"), code=entry.get("code"))
            for entry in response
        ]


@alru_cache
async def get_rights_statements() -> List[ParsedReferenceData]:
    rights_statements = await fetch_access_rights_from_reference_data()
    return ParsedReferenceData.from_rights_statement_list(rights_statements)


@alru_cache
async def get_los_paths() -> List[dict]:
    los_themes = await fetch_themes_and_topics_from_reference_data()
    return los_themes


@alru_cache
async def get_file_types() -> List[dict]:
    file_types = await fetch_file_types_from_reference_data()
    return FileTypes.from_reference_data_response(file_types)


@alru_cache
async def get_media_types() -> List[dict]:
    media_types = await fetch_media_types_from_reference_data()
    return MediaTypes.from_reference_data_response(media_types)


def clean_uri(uri_from_sparql: str) -> str:
    return uri_from_sparql.replace("<", "").replace(">", "")


async def get_access_rights_code(uri: str) -> Optional[str]:
    raw_uri = clean_uri(uri)
    access_rights = await get_rights_statements()
    try:
        ar_idx = access_rights.index(raw_uri)
        return access_rights[ar_idx].ref_value
    except ValueError:
        return None


def get_los_path(uri_list: List[str], los_themes: List[dict]) -> List[str]:
    uri_to_los_path_list: List = []
    for uri in uri_list:
        raw_uri = clean_uri(uri)
        try:
            theme_reference = [
                theme["losPaths"] for theme in los_themes if theme.get("uri") == raw_uri
            ]
            if len(theme_reference) > 0:
                uri_to_los_path_list.extend(*theme_reference)
        except ValueError:
            continue
    return uri_to_los_path_list
