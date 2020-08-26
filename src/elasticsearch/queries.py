import abc

from src.elasticsearch.utils import EsMappings
from src.rdf_namespaces import JSON_LD, ContentKeys
from src.utils import ServiceKey


class AggregationQuery:
    def __init__(self, report_type: ServiceKey):
        # TODO : new last week
        self.aggregations = {
            EsMappings.ORG_PATH: {
                "terms": {
                    "field": "orgPath.keyword",
                    "missing": "MISSING",
                    "size": 1000000000
                }
            }
        }

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
                                                       "-right/PUBLIC "
                    }
                },
                {
                    "term": {
                        "openLicense": "true"
                    }
                }
            ]
        }
    }
    }
