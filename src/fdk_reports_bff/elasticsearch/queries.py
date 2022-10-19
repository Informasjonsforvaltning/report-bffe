import abc
from typing import Any, Optional

from fdk_reports_bff.service.utils import ContentKeys, ServiceKey, ThemeProfile


class EsMappings:
    PART_OF_CATALOG = "partOfCatalog"
    BUCKETS = "buckets"
    AGGREGATIONS = "aggregations"
    DOC_COUNT = "doc_count"
    ORGANIZATION_ID = "orgId"
    TIME_SERIES = "timeseries"
    FORMAT = "format"
    LOS = "los"
    VALUE_KEYWORD = ".value.keyword"
    NODE_URI = "nodeUri"
    ORG_PATH = "orgPath"
    LOS_PATH = "losPaths"
    MISSING = "MISSING"
    OPEN_LICENSE = "OpenLicense"
    FIRST_HARVESTED = "firstHarvested"
    TITLE = "title"
    MEDIATYPE = "mediaType"
    ACCESS_RIGHTS = "accessRights"
    PROVENANCE = "provenance"
    SUBJECT = "subject"
    DISTRIBUTION = "distribution"
    THEME = "theme"
    TRANSPORTPORTAL = "transportportal"
    TIMESTAMP = "timestamp"


DATASET_AGGREGATION_FIELDS = [
    EsMappings.ORG_PATH,
    EsMappings.ORGANIZATION_ID,
    EsMappings.LOS,
    EsMappings.ACCESS_RIGHTS,
    EsMappings.PROVENANCE,
    EsMappings.TITLE,
    EsMappings.SUBJECT,
    EsMappings.DISTRIBUTION,
    EsMappings.THEME,
    EsMappings.NODE_URI,
    EsMappings.OPEN_LICENSE,
    EsMappings.FORMAT,
    EsMappings.PART_OF_CATALOG,
    EsMappings.FIRST_HARVESTED,
    EsMappings.TRANSPORTPORTAL,
]

DATASERVICE_AGGREGATION_FIELDS = [
    EsMappings.ORG_PATH,
    EsMappings.ORGANIZATION_ID,
    EsMappings.TITLE,
    EsMappings.FIRST_HARVESTED,
    EsMappings.FORMAT,
]

INFORMATION_MODEL_AGGREGATION_FIELDS = [
    EsMappings.ORG_PATH,
    EsMappings.ORGANIZATION_ID,
    EsMappings.TITLE,
    EsMappings.FIRST_HARVESTED,
]

CONCEPT_AGGREGATION_FIELDS = [
    EsMappings.ORG_PATH,
    EsMappings.ORGANIZATION_ID,
    EsMappings.FIRST_HARVESTED,
]


class Query(metaclass=abc.ABCMeta):
    def __init__(self: Any) -> None:
        self.aggregations = None
        self.query = None

    def add_filters(
        self: Any, orgpath: Any, themes: Any, theme_profile: Any, organization_id: Any
    ) -> None:
        if orgpath or themes or theme_profile or organization_id:
            self.query = {"bool": {"filter": []}}
            if themes:
                self.query["bool"]["filter"].extend(
                    get_los_path_filter(themes_str=themes)
                )
            if orgpath:
                self.query["bool"]["filter"].append(get_org_path_filter(orgpath))
            if theme_profile:
                self.query["bool"]["filter"].append(
                    get_theme_profile_filter(ThemeProfile.TRANSPORT)
                )
            if organization_id:
                self.query["bool"]["filter"].append(
                    get_term_query(EsMappings.ORGANIZATION_ID, organization_id)
                )

    def build(self: Any) -> dict:
        body = {"size": 0, "aggregations": self.aggregations}
        if self.query:
            body["query"] = self.query
        return body


class AggregationQuery(Query):
    def __init__(
        self: Any,
        report_type: str,
        orgpath: Any = None,
        theme: Any = None,
        theme_profile: Any = None,
        organization_id: Any = None,
    ) -> None:
        super().__init__()
        self.aggregations = {
            EsMappings.ORG_PATH: {
                "terms": {
                    "field": EsMappings.ORG_PATH,
                    "missing": "MISSING",
                    "size": 100000,
                }
            },
            ContentKeys.NEW_LAST_WEEK: get_last_x_days_filter(
                key=f"{EsMappings.FIRST_HARVESTED}.value", days=7
            ),
            ContentKeys.CATALOGS: {
                "terms": {
                    "field": f"{EsMappings.PART_OF_CATALOG}.id.keyword",
                    "missing": "MISSING",
                    "size": 100000,
                }
            },
            ContentKeys.ORGANIZATION_COUNT: {
                "cardinality": {"field": f"{EsMappings.ORGANIZATION_ID}.keyword"}
            },
        }
        if report_type == ServiceKey.DATA_SETS:
            self.__add_datasets_aggregation()
        elif report_type == ServiceKey.DATA_SERVICES:
            self.__add_dataservice_aggregation()
        self.query = None
        self.add_filters(orgpath, theme, theme_profile, organization_id)

    def __add_datasets_aggregation(self: Any) -> None:
        self.aggregations[
            ContentKeys.ACCESS_RIGHTS_CODE
        ] = AggregationQuery.json_rdf_terms_aggregation(EsMappings.ACCESS_RIGHTS)
        self.aggregations[ContentKeys.NATIONAL_COMPONENT] = {
            "filter": {
                "term": {
                    AggregationQuery.es_keyword_key(
                        EsMappings.PROVENANCE
                    ): "http://data.brreg.no/datakatalog/provinens/nasjonal"
                }
            }
        }
        self.aggregations[ContentKeys.WITH_SUBJECT] = {
            "filter": {"exists": {"field": EsMappings.SUBJECT}}
        }
        self.aggregations[ContentKeys.LOS_PATH] = {
            "terms": {"field": EsMappings.LOS, "missing": "MISSING", "size": 100000}
        }
        self.aggregations[ContentKeys.OPEN_DATA] = open_data_aggregation()
        self.aggregations[ContentKeys.FORMAT] = {
            "terms": {
                "field": f"{EsMappings.FORMAT}.keyword",
                "missing": "MISSING",
                "size": 100000,
            }
        }

    def __add_dataservice_aggregation(self: Any) -> None:
        self.aggregations[ContentKeys.FORMAT] = {
            "terms": {
                "field": f"{EsMappings.FORMAT}.keyword",
                "missing": "MISSING",
                "size": 100000,
            }
        }

    @staticmethod
    def es_keyword_key(json_ld_key: str) -> str:
        return f"{json_ld_key}{EsMappings.VALUE_KEYWORD}"

    @staticmethod
    def json_rdf_terms_aggregation(json_ld_field: str, size: int = None) -> dict:
        return {
            "terms": {
                "field": AggregationQuery.es_keyword_key(json_ld_field),
                "missing": EsMappings.MISSING,
                "size": size or 10,
            }
        }


class TimeSeriesQuery(Query):
    def __init__(
        self: Any,
        series_field: Any,
        orgpath: Any,
        theme: Any,
        theme_profile: Any,
        organization_id: Any,
    ) -> None:
        super().__init__()
        self.aggregations = {
            f"{EsMappings.TIME_SERIES}": {
                "date_histogram": {"field": series_field, "calendar_interval": "month"}
            }
        }
        self.add_filters(orgpath, theme, theme_profile, organization_id)


def org_path_aggregation() -> dict:
    return {
        "terms": {
            "field": "orgPath.keyword",
            "missing": EsMappings.MISSING,
            "size": 1000000000,
        }
    }


def open_data_aggregation() -> dict:
    return {
        "filter": {
            "bool": {
                "must": [
                    {
                        "term": {
                            AggregationQuery.es_keyword_key(
                                EsMappings.ACCESS_RIGHTS
                            ): "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                        }
                    },
                    {"term": {EsMappings.OPEN_LICENSE: "true"}},
                ]
            }
        }
    }


def get_last_x_days_filter(key: str, days: int) -> dict:
    range_str = f"now-{days}d/d"
    return {"filter": {"range": {key: {"gte": range_str, "lt": "now+1d/d"}}}}


def get_los_path_filter(
    themes_str: Optional[str] = None, profile_themes_list: Optional[list] = None
) -> list:
    if themes_str is not None:
        themes_list = themes_str.split(",")
    elif profile_themes_list is not None:
        themes_list = profile_themes_list
    else:
        return []
    terms = []
    for theme in themes_list:
        terms.append({"term": {EsMappings.LOS: theme}})
    return terms


def get_org_path_filter(org_path: str) -> dict:
    if org_path == EsMappings.MISSING:
        return must_not_filter(EsMappings.ORG_PATH)
    return {"term": {EsMappings.ORG_PATH: org_path}}


def get_theme_profile_filter(profile: str) -> dict:
    if profile == ThemeProfile.TRANSPORT:
        return {
            "bool": {
                "must": [
                    {"term": {EsMappings.TRANSPORTPORTAL: "true"}},
                ]
            }
        }
    else:
        return {}


def get_term_query(field: str, value: str) -> dict:
    return {"term": {f"{field}.keyword": {"value": value}}}


def must_not_filter(filter_key: str) -> dict:
    missing_filter = {"bool": {"must_not": {"exists": {"field": filter_key}}}}
    return missing_filter
