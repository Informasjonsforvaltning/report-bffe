import itertools
import re
from typing import List

from src.referenced_data_store import get_org_path, get_access_rights_code, get_los_path


class ContentKeys:
    FORMAT = "format"
    WITH_SUBJECT = "withSubject"
    OPEN_DATA = "opendata"
    TOTAL = "total"
    NEW_LAST_WEEK = "new_last_week"
    NATIONAL_COMPONENT = "nationalComponent"
    ORGANIZATION = "organization"
    COUNT = "count"
    VALUE = "value"
    ACCESS_RIGHTS_CODE = "code"
    TIME_SERIES_X_AXIS = "date"
    TIME_SERIES_Y_AXIS = "count"
    THEME = "theme"


def parse_sparql_formats_count(sparql_result: dict) -> list:
    bindings = sparql_result["results"]["bindings"]
    format_list = [KeyCountObject.from_sparql(key=ContentKeys.FORMAT,
                                              sparql_result=x) for x in bindings]
    return KeyCountObject.reduce_to_dicts(format_list)


def parse_sparql_single_results(sparql_results: dict) -> dict:
    bindings = sparql_results["results"]["bindings"]
    parsed_content = {}
    for result in bindings:
        try:
            parsed_content[ContentKeys.WITH_SUBJECT] = result[ContentKeys.WITH_SUBJECT]["value"]
            parsed_content[ContentKeys.TOTAL] = result[ContentKeys.TOTAL]["value"]
            parsed_content[ContentKeys.NEW_LAST_WEEK] = result[ContentKeys.NEW_LAST_WEEK]["value"]
            parsed_content[ContentKeys.NATIONAL_COMPONENT] = result[ContentKeys.NATIONAL_COMPONENT]["value"]
            parsed_content[ContentKeys.OPEN_DATA] = result[ContentKeys.OPEN_DATA]["value"]
        except KeyError:
            continue

    return parsed_content


async def parse_sparql_catalogs_count(sparql_result: dict) -> list:
    bindings = sparql_result["results"]["bindings"]
    catalog_list = [await KeyCountObject.with_reference_key(reference_function=get_org_path,
                                                            key=ContentKeys.ORGANIZATION,
                                                            sparql_result=x)
                    for x in bindings]
    return KeyCountObject.expand_with_hierarchy(catalog_list)


async def parse_sparql_access_rights_count(sparql_result: dict) -> list:
    bindings = sparql_result["results"]["bindings"]
    access_rights_list = [await KeyCountObject.with_reference_key(reference_function=get_access_rights_code,
                                                                  key=ContentKeys.ACCESS_RIGHTS_CODE,
                                                                  sparql_result=x)
                          for x in bindings]
    return KeyCountObject.to_dicts(access_rights_list)


async def parse_sparql_themes_and_topics_count(sparql_results: dict) -> list:
    bindings = sparql_results["results"]["bindings"]
    themes_list = [await KeyCountObject.with_reference_list_key(reference_function=get_los_path,
                                                                key=ContentKeys.THEME,
                                                                sparql_result=x
                                                                )
                   for x in bindings]
    flattened_list = itertools.chain.from_iterable(themes_list)
    return KeyCountObject.expand_with_hierarchy(flattened_list)


def parse_sparql_time_series(sparql_result: dict) -> list:
    bindings = sparql_result["results"]["bindings"]
    return [{"xAxis": x[ContentKeys.TIME_SERIES_X_AXIS][ContentKeys.VALUE],
             "yAxis": x[ContentKeys.TIME_SERIES_Y_AXIS][ContentKeys.VALUE]}
            for x in bindings]


class KeyCountObject:
    def __init__(self, key: str, count: str, normalize=False):
        if normalize:
            self.key = key.upper()
        else:
            self.key = key
        self.count = int(count)

    def __eq__(self, other):
        if other is None:
            return False
        elif isinstance(other, str):
            return re.findall(other, self.key).__len__() > 0
        else:
            return other.key == self.key

    def get_count_with_hierarchy(self) -> List['KeyCountObject']:
        hierarchy_parts = [x for x in self.key.split("/")]
        hierarchy_list = []
        for i, v in enumerate(hierarchy_parts):
            hierarchy_key = '/'.join(hierarchy_parts[0: i + 1])
            hierarchy_list.append(KeyCountObject(key=hierarchy_key, count=self.count))

        return hierarchy_list

    @staticmethod
    def reduce_to_dicts(objects: list):
        reduced_list = []
        while len(objects) > 0:
            current = objects.pop()
            if current in reduced_list:
                existing = reduced_list[reduced_list.index(current)]
                existing.count += current.count
            else:
                reduced_list.append(current)
        return [x.__dict__ for x in reduced_list if x]

    @staticmethod
    def expand_with_hierarchy(objects: List['KeyCountObject']):
        hierarchies = []
        aggregated_hierarchies = []
        for obj in objects:
            if obj:
                hierarchies.extend(obj.get_count_with_hierarchy())
        for part in hierarchies:
            try:
                idx = aggregated_hierarchies.index(part.key)
                aggregated_hierarchies[idx].count += part.count
            except ValueError:
                aggregated_hierarchies.append(part)
        return [x.__dict__ for x in aggregated_hierarchies]

    @staticmethod
    def from_sparql(key: str, sparql_result: dict):
        return KeyCountObject(key=sparql_result[key]["value"],
                              count=sparql_result[ContentKeys.COUNT][ContentKeys.VALUE],
                              normalize=True)

    @staticmethod
    async def with_reference_key(reference_function, key, sparql_result):
        reference = await reference_function(sparql_result[key][ContentKeys.VALUE])
        if reference:
            return KeyCountObject(key=reference, count=sparql_result[ContentKeys.COUNT][ContentKeys.VALUE])
        else:
            return None

    @staticmethod
    async def with_reference_list_key(reference_function, key, sparql_result):
        references = await reference_function(sparql_result[key][ContentKeys.VALUE])
        key_count_objects = []
        if references:
            for ref in references:
                key_count_objects.append(
                    KeyCountObject(key=ref, count=sparql_result[ContentKeys.COUNT][ContentKeys.VALUE]))
            return key_count_objects
        else:
            return None

    @staticmethod
    def to_dicts(objects: list):
        return [x.__dict__ for x in objects if x]
