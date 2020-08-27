import abc

from src.elasticsearch.utils import EsMappings
from src.rdf_namespaces import JSON_LD, ContentKeys
from src.utils import ServiceKey

DATASET_AGGREGATION_FIELDS = [EsMappings.ORG_PATH, EsMappings.LOS, JSON_LD.DCT.accessRights,
                              JSON_LD.DCT.provenance, JSON_LD.DCT.subject, JSON_LD.DCAT.distribution,
                              JSON_LD.DCAT.theme, EsMappings.NODE_URI, EsMappings.RECORD, EsMappings.OPEN_LICENSE]

CATALOG_RECORD_AGGREGATION_FIELDS = [
    JSON_LD.DCT.issued
]


class AggregationQuery:
    def __init__(self, report_type: ServiceKey):
        self.aggregations = {EsMappings.ORG_PATH: {
            "terms": {
                "field": "orgPath.keyword",
                "missing": "MISSING",
                "size": 1000000000
            }
        }, ContentKeys.NEW_LAST_WEEK: get_last_x_days_filter(key=f"{EsMappings.RECORD}.{JSON_LD.DCT.issued}.value",
                                                             days=7)}

        if report_type == ServiceKey.DATA_SETS:
            self.__add_datasets_aggregation()

    def __add_datasets_aggregation(self):
        self.aggregations[ContentKeys.ACCESS_RIGHTS_CODE] = AggregationQuery.json_ld_terms_aggregation(
            JSON_LD.DCT.accessRights)
        self.aggregations[ContentKeys.NATIONAL_COMPONENT] = {
            "filter": {
                "term": {
                    AggregationQuery.es_keyword_key(
                        JSON_LD.DCT.provenance): "http://data.brreg.no/datakatalog/provinens/nasjonal"
                }
            }
        }
        self.aggregations[ContentKeys.WITH_SUBJECT] = {
            "filter": {
                "exists": {
                    "field": JSON_LD.DCT.subject
                }
            }
        }
        los_path_field = f"{EsMappings.LOS}.{EsMappings.LOS_PATH}"
        self.aggregations[ContentKeys.LOS_PATH] = {
            "terms": {
                "field": los_path_field
            }
        }
        self.aggregations[ContentKeys.OPEN_DATA] = open_data_aggregation()

    def build(self):
        return {
            "size": 0,
            "aggregations": self.aggregations
        }

    @staticmethod
    def es_keyword_key(json_ld_key: str):
        return f"{json_ld_key}{EsMappings.VALUE_KEYWORD}"

        # TODO themesAndTopics, formats, open_data

    @staticmethod
    def json_ld_terms_aggregation(json_ld_field: str, size: int = None):
        return {
            "terms": {
                "field": AggregationQuery.es_keyword_key(json_ld_field),
                "missing": EsMappings.MISSING,
                "size": size or 10
            }
        }


def org_path_aggregation() -> dict:
    return {
        "terms": {
            "field": "orgPath",
            "missing": EsMappings.MISSING,
            "size": 1000000000
        }
    }


def open_data_aggregation() -> dict:
    return {"filter": {
        "bool": {
            "must": [
                {
                    "term": {
                        AggregationQuery.es_keyword_key(
                            JSON_LD.DCT.accessRights): "http://publications.europa.eu/resource/authority/access"
                                                       "-right/PUBLIC"
                    }
                },
                {
                    "term": {
                        EsMappings.OPEN_LICENSE: "true"
                    }
                }
            ]
        }
        }
    }


def get_last_x_days_filter(key: str, days: int):
    range_str = f"now-{days}d/d"
    return {"filter": {
        "range": {
            key: {
                "gte": range_str,
                "lt": "now/d"
            }
        }
    }}
