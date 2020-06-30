from src.referenced_data_store import get_organizations, get_org_path, get_access_rights_code


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


def parse_sparql_formats_count(sparql_result: dict) -> list:
    bindings = sparql_result["results"]["bindings"]
    format_list = [KeyCountObject.from_sparql(ContentKeys.FORMAT, x) for x in bindings]
    return KeyCountObject.reduce_to_dicts(format_list)


def parse_sparql_single_results(sparql_results: dict) -> dict:
    bindings = sparql_results["results"]["bindings"]
    parsed_content = {}
    for result in bindings:
        parsed_content[ContentKeys.WITH_SUBJECT] = result[ContentKeys.WITH_SUBJECT]["value"]
        parsed_content[ContentKeys.TOTAL] = result[ContentKeys.TOTAL]["value"]
        parsed_content[ContentKeys.NEW_LAST_WEEK] = result[ContentKeys.NEW_LAST_WEEK]["value"]
        parsed_content[ContentKeys.NATIONAL_COMPONENT] = result[ContentKeys.NATIONAL_COMPONENT]["value"]
    return parsed_content


def parse_sparql_catalogs_count(sparql_result: dict) -> list:
    bindings = sparql_result["results"]["bindings"]
    catalog_list = [KeyCountObject.with_reference_key(reference_function=get_org_path,
                                                      key=ContentKeys.ORGANIZATION,
                                                      sparql_result=x)
                    for x in bindings]
    return KeyCountObject.reduce_to_dicts(catalog_list)


def parse_sparql_access_rights_count(sparql_result: dict) -> list:
    bindings = sparql_result["results"]["bindings"]
    access_rights_list = [KeyCountObject.with_reference_key(reference_function=get_access_rights_code,
                                                            key=ContentKeys.ACCESS_RIGHTS_CODE,
                                                            sparql_result=x)
                          for x in bindings]
    return KeyCountObject.to_dicts(access_rights_list)


def parse_sparql_themes_and_topics(sparql_results: dict) -> list:
    pass


def parse_sparql_time_series(sparql_result: dict) -> list:
    bindings = sparql_result["results"]["bindings"]
    return [{"xAxis": x[ContentKeys.TIME_SERIES_X_AXIS][ContentKeys.VALUE],
             "yAxis": x[ContentKeys.TIME_SERIES_Y_AXIS][ContentKeys.VALUE]}
            for x in bindings]


class KeyCountObject:
    def __init__(self, key: str, count: str):
        self.key = key.upper()
        self.count = int(count)

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return other.key == self.key

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
    def from_sparql(key: str, sparql_result: dict):
        return KeyCountObject(key=sparql_result[key]["value"],
                              count=sparql_result[ContentKeys.COUNT][ContentKeys.VALUE])

    @staticmethod
    def with_reference_key(reference_function, key, sparql_result):
        reference = reference_function(sparql_result[key][ContentKeys.VALUE])
        if reference:
            return KeyCountObject(key=reference, count=sparql_result[ContentKeys.COUNT][ContentKeys.VALUE])
        else:
            return None

    @staticmethod
    def to_dicts(objects: list):
        return [x.__dict__ for x in objects if x]
