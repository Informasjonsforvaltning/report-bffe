from typing import List


class Response:
    def __init__(self, totalObjects: int = None, newLastWeek: int = None, catalogs: list = None):
        if totalObjects:
            self.totalObjects = totalObjects
        if newLastWeek:
            self.newLastWeek = newLastWeek
        if catalogs:
            self.catalogs = catalogs

    def populate_from_es(self, es_result: dict) -> 'Response':
        self.totalObjects = es_result["page"]["totalElements"]
        harvest_aggs = es_result["aggregations"]["firstHarvested"]["buckets"]
        self.newLastWeek = [x["count"] for x in harvest_aggs if x["key"] == "last7days"][0]
        self.catalogs = es_result["aggregations"]["orgPath"]["buckets"]


class InformationModelResponse(Response):
    def __init__(self, totalObjects: int = None, newLastWeek: int = None, catalogs: list = None):
        super().__init__(totalObjects, newLastWeek, catalogs)

    @staticmethod
    def from_es(es_result: dict):
        response = InformationModelResponse()
        response.populate_from_es(es_result=es_result)
        return response


class ConceptResponse(Response):
    def __init__(self, totalObjects: int = None, newLastWeek: int = None, catalogs: list = None,
                 most_in_use: list = None):
        super().__init__(totalObjects, newLastWeek, catalogs)
        if most_in_use:
            self.mostInUse = most_in_use

    @staticmethod
    def from_es(es_result: dict, most_in_use: dict):
        response = ConceptResponse()
        response.populate_from_es(es_result=es_result)
        response.mostInUse = ConceptResponse.parse_reference_list(most_in_use)
        return response

    @staticmethod
    def parse_reference_list(result_from_harvester: dict) -> list:
        concepts = result_from_harvester["_embedded"]["concepts"]
        reference_list = []
        for concept in concepts:
            ref = {
                "prefLabel": concept["prefLabel"],
                "uri": concept["uri"]
            }
            reference_list.append(ref)
        return reference_list


class DataSetResponse(Response):
    def __init__(self, dist_formats: List[dict], single_aggregations: dict, catalogs: List[dict], themes: List[dict]):
        super().__init__(totalObjects=single_aggregations["total"],
                         newLastWeek=single_aggregations["new_last_week"],
                         catalogs=catalogs
                         )
        self.nationalComponent = single_aggregations["nationalComponent"]
        self.withSubject = single_aggregations["withSubject"]
        self.themesAndTopicsCount = themes
        self.formats = dist_formats


