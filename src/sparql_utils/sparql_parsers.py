import itertools
import re
from datetime import datetime
from typing import List

from src.referenced_data_store import get_org_path, get_access_rights_code, get_los_path
from src.sparql_utils import ContentKeys
from src.utils import ServiceKey


def parse_sparql_formats_count(sparql_result: dict) -> list:
    if sparql_result is None:
        return
    bindings = sparql_result["results"]["bindings"]
    format_list = [KeyCountObject.from_sparql(key=ContentKeys.FORMAT,
                                              sparql_result=x) for x in bindings]
    return KeyCountObject.reduce_to_dicts(format_list)


def parse_sparql_single_statistic(key: ContentKeys, sparql_result: dict) -> list:
    if sparql_result is None:
        return
    bindings = sparql_result["results"]["bindings"]
    return bindings[0][key][ContentKeys.VALUE]


async def parse_sparql_catalogs_count(sparql_result: dict, content_type: ServiceKey) -> list:
    if sparql_result is None or len(sparql_result) == 0:
        return
    bindings = sparql_result["results"]["bindings"]
    catalog_list = [await get_organization(sparql_result=x, content_type=content_type)
                    for x in bindings]
    return KeyCountObject.expand_with_hierarchy(catalog_list)


async def get_organization(sparql_result: dict, content_type: ServiceKey):
    try:
        src_uri = sparql_result[ContentKeys.SRC_ORGANIZATION][ContentKeys.VALUE]
    except KeyError:
        src_uri = None
    reference = await get_org_path(uri=sparql_result[ContentKeys.ORGANIZATION_URI][ContentKeys.VALUE],
                                   src_uri=src_uri,
                                   content_type=content_type,
                                   name=sparql_result[ContentKeys.ORG_NAME][ContentKeys.VALUE]
                                   )
    if reference:
        return KeyCountObject(key=reference, count=sparql_result[ContentKeys.COUNT][ContentKeys.VALUE])
    else:
        return None


async def parse_sparql_access_rights_count(sparql_result: dict) -> list:
    if sparql_result is None:
        return
    bindings = sparql_result["results"]["bindings"]
    access_rights_list = [await KeyCountObject.with_reference_key(reference_function=get_access_rights_code,
                                                                  key=ContentKeys.ACCESS_RIGHTS_CODE,
                                                                  sparql_result=x)
                          for x in bindings]
    return KeyCountObject.to_dicts(access_rights_list)


def remove_none_values(iterable) -> list:
    values = []
    try:
        for item in iterable:
            if item:
                values.append(item)
    except TypeError:
        pass
    return values


async def parse_sparql_themes_and_topics_count(sparql_results: dict) -> list:
    if sparql_results is None:
        return
    bindings = sparql_results["results"]["bindings"]
    themes_list = [await KeyCountObject.with_reference_list_key(reference_function=get_los_path,
                                                                key=ContentKeys.THEME,
                                                                sparql_result=x
                                                                )
                   for x in bindings]
    flattened_list = itertools.chain.from_iterable(themes_list)
    return KeyCountObject.expand_with_hierarchy(remove_none_values(flattened_list))


def parse_sparql_time_series(sparql_result: dict) -> list:
    if sparql_result is None:
        return
    bindings = sparql_result["results"]["bindings"]
    return [ParsedDataPoint.from_result_entry(x)
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
            if v == "":
                continue
            else:
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


class ParsedDataPoint:
    def __init__(self, month, year, count):
        try:
            self.month = int(month)
            self.year = int(year)
        except TypeError:
            self.month = month
            self.year = year

        self.count = count

    def __str__(self):
        month_str = str(self.month)
        if len(month_str) == 1:
            month_str = f"0{month_str}"
        date_strings = ("01", month_str, str(self.year))
        return ".".join(date_strings)

    def response_dict(self):
        return {
            ContentKeys.TIME_SERIES_X_AXIS: str(self),
            ContentKeys.TIME_SERIES_Y_AXIS: self.count
        }

    def get_next_month(self):
        next_month = self.month + 1
        next_year = self.year
        if next_month == 13:
            next_month = 1
            next_year += 1
        return ParsedDataPoint(month=next_month, year=next_year, count=0)

    def __eq__(self, other: 'ParsedDataPoint'):
        return self.month == other.month and self.year == other.year

    @staticmethod
    def from_result_entry(entry: dict):
        return ParsedDataPoint(month=entry[ContentKeys.TIME_SERIES_MONTH]["value"],
                               year=entry[ContentKeys.TIME_SERIES_YEAR]["value"],
                               count=entry[ContentKeys.COUNT]["value"]
                               )

    @staticmethod
    def from_date_time(date_time: datetime):
        return ParsedDataPoint(month=date_time.month,
                               year=date_time.year,
                               count=0
                               )
