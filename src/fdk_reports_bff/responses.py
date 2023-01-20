from datetime import datetime
from typing import Any, List, Optional

from fdk_reports_bff.elasticsearch.queries import EsMappings
from fdk_reports_bff.service.utils import ParsedDataPoint, ServiceKey, ThemeProfile


class Response:
    def __init__(
        self: Any,
        total_objects: Optional[int],
        organization_count: Optional[int],
        new_last_week: Optional[int],
        catalogs: Optional[List[dict]],
        org_paths: Optional[List[dict]],
    ) -> None:
        self.totalObjects = total_objects
        self.newLastWeek = new_last_week
        self.catalogs = catalogs or []
        self.orgPaths = org_paths or []
        self.organizationCount = organization_count

    def populate_from_es(self: Any, es_result: dict) -> None:
        self.totalObjects = es_result["page"]["totalElements"]
        harvest_aggs = es_result["aggregations"]["firstHarvested"]["buckets"]
        self.newLastWeek = [
            x["count"] for x in harvest_aggs if x["key"] == "last7days"
        ][0]
        self.catalogs = es_result["aggregations"]["orgPath"]["buckets"]


class InformationModelResponse(Response):
    def __init__(
        self: Any,
        total_objects: Optional[int] = None,
        new_last_week: Optional[int] = None,
        catalogs: Optional[List[dict]] = None,
        org_paths: Optional[List[dict]] = None,
        organization_count: int = 0,
    ) -> None:
        super().__init__(
            total_objects, organization_count, new_last_week, catalogs, org_paths
        )

    @staticmethod
    def from_es(es_result: dict) -> Any:
        response = InformationModelResponse()
        response.populate_from_es(es_result=es_result)
        return response

    def json(self: Any) -> dict:
        serialized = self.__dict__
        return serialized

    @staticmethod
    def empty_response() -> Any:
        return InformationModelResponse(
            total_objects=0, new_last_week=0, catalogs=None, org_paths=None
        )


class DataServiceResponse(Response):
    def __init__(
        self: Any,
        total_objects: Optional[int] = None,
        new_last_week: Optional[int] = None,
        catalogs: Optional[List[dict]] = None,
        org_paths: Optional[List[dict]] = None,
        organization_count: int = 0,
        formats: Optional[List[dict]] = None,
    ) -> None:
        super().__init__(
            total_objects, organization_count, new_last_week, catalogs, org_paths
        )
        self.formats = formats or []

    @staticmethod
    def from_es(es_result: dict) -> Any:
        response = DataServiceResponse()
        response.populate_from_es(es_result=es_result)
        return response

    def json(self: Any) -> dict:
        serialized = self.__dict__
        return serialized

    @staticmethod
    def empty_response() -> Any:
        return DataServiceResponse(
            total_objects=0, new_last_week=0, catalogs=None, org_paths=None
        )


class ConceptResponse(Response):
    def __init__(
        self: Any,
        total_objects: int = 0,
        new_last_week: Optional[int] = None,
        catalogs: Optional[list] = None,
        most_in_use: Optional[list] = None,
        org_paths: Optional[list] = None,
        organization_count: int = 0,
    ) -> None:
        super().__init__(
            total_objects, organization_count, new_last_week, catalogs, org_paths
        )
        if most_in_use:
            self.mostInUse = most_in_use

    @staticmethod
    def from_es(es_result: dict, most_in_use: dict) -> Any:
        response = ConceptResponse()
        response.populate_from_es(es_result=es_result)
        response.mostInUse = ConceptResponse.parse_reference_list(most_in_use)
        return response

    @staticmethod
    def parse_reference_list(result_from_harvester: dict) -> list:
        concepts = result_from_harvester["_embedded"]["concepts"]
        reference_list = []
        for concept in concepts:
            ref = {"prefLabel": concept["prefLabel"], "uri": concept["uri"]}
            reference_list.append(ref)
        return reference_list

    def json(self: Any) -> Any:
        serialized = self.__dict__
        return serialized

    @staticmethod
    def empty_response() -> Any:
        return ConceptResponse(
            total_objects=0,
            new_last_week=0,
            catalogs=None,
            most_in_use=None,
            org_paths=None,
            organization_count=0,
        )


class DataSetResponse(Response):
    def __init__(
        self: Any,
        dist_formats: Optional[List[dict]],
        total: int,
        organization_count: int,
        new_last_week: int,
        opendata: str,
        national_component: str,
        with_subject: str,
        catalogs: Optional[List[dict]],
        org_paths: Optional[List[dict]],
        themes: Optional[List[dict]],
        access_rights: Optional[List[dict]],
        theme_profile: Optional[ThemeProfile] = None,
    ) -> None:
        super().__init__(
            total_objects=total,
            new_last_week=new_last_week,
            catalogs=catalogs,
            org_paths=org_paths,
            organization_count=organization_count,
        )

        self.opendata = opendata
        self.nationalComponent = national_component
        self.withSubject = with_subject
        self.themesAndTopicsCount = themes or []
        self.formats = dist_formats or []
        self.accessRights = access_rights or []
        if theme_profile is not None:
            self.customize_for_theme_profile(theme_profile)

    def customize_for_theme_profile(self: Any, theme_profile: ThemeProfile) -> None:
        if theme_profile == ThemeProfile.TRANSPORT:
            theme_profile_themes = [
                theme
                for theme in self.themesAndTopicsCount
                if theme.get("key") in ThemeProfile.TRANSPORT_THEMES
            ]
            self.themesAndTopicsCount = theme_profile_themes

    def json(self: Any) -> dict:
        serialized = self.__dict__
        return serialized

    @staticmethod
    def empty_response() -> Any:
        return DataSetResponse(
            dist_formats=None,
            total=0,
            organization_count=0,
            new_last_week=0,
            opendata="0",
            national_component="0",
            with_subject="0",
            catalogs=None,
            org_paths=None,
            themes=None,
            access_rights=None,
        )


class TimeSeriesResponse:
    def __init__(self: Any, es_time_series: List[dict], report_type: str) -> None:
        self.time_series: List = []
        self.type = report_type
        self.last_data_point: ParsedDataPoint = None
        self.parse_es_time_series(es_time_series=es_time_series)
        self.add_months_from_last_data_point_to_now()

    def parse_es_time_series(self: Any, es_time_series: dict) -> None:
        last_count = 0
        time_buckets = es_time_series[EsMappings.AGGREGATIONS][EsMappings.TIME_SERIES][
            EsMappings.BUCKETS
        ]
        for time_bucket in time_buckets:
            if self.type == ServiceKey.DATA_SETS or self.type == ServiceKey.CONCEPTS:
                new_data_point = ParsedDataPoint(
                    es_bucket=time_bucket, last_month_count=0
                )
            else:
                new_data_point = ParsedDataPoint(
                    es_bucket=time_bucket, last_month_count=last_count
                )
            last_count = new_data_point.y_axis
            self.add(new_data_point)

    def add(self: Any, parsed_entry: Any) -> None:
        if len(self.time_series) == 0:
            self.time_series.append(parsed_entry.response_dict())
            self.last_data_point = parsed_entry
        elif parsed_entry == self.last_data_point.get_next_month():
            self.time_series.append(parsed_entry.response_dict())
            self.last_data_point = parsed_entry
        else:
            while self.last_data_point.get_next_month() != parsed_entry:
                next_month = self.last_data_point.get_next_month()
                self.time_series.append(next_month.response_dict())
                self.last_data_point = next_month
            self.time_series.append(parsed_entry.response_dict())
            self.last_data_point = parsed_entry

    def add_months_from_last_data_point_to_now(self: Any) -> None:
        if self.last_data_point is not None:
            now_data_point = ParsedDataPoint.from_date_time(
                datetime.now(), self.last_data_point
            )

            while self.last_data_point != now_data_point:
                next_month = self.last_data_point.get_next_month()
                self.time_series.append(next_month.response_dict())
                self.last_data_point = next_month

    def json(self: Any) -> List[dict]:
        return self.time_series
