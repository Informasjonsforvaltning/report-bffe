from datetime import datetime

from dateutil import parser
from flask import Flask
import pytest


class TestDatasetsReport:
    @pytest.mark.integration
    def test_report_has_correct_format(self, client: Flask, docker_service, api):
        result = client.get("/report/datasets")
        assert result.status_code == 200
        content = result.json
        keys = result.json.keys()
        assert "totalObjects" in keys
        assert "newLastWeek" in keys
        assert "nationalComponent" in keys
        assert "opendata" in keys
        assert "catalogs" in keys
        assert "withSubject" in keys
        assert "accessRights" in keys
        assert "themesAndTopicsCount" in keys
        assert "orgPaths" in keys
        assert "organizationCount" in keys
        assert "formats" in keys
        assert len(content.get("orgPaths")) > len(content.get("catalogs"))
        assert content.get("organizationCount") < len(content.get("orgPaths"))
        assert content.get("organizationCount") > len(content.get("catalogs"))
        assert len(content.get("catalogs")) > 1
        assert content.get("totalObjects") == 1251
        assert content.get("nationalComponent") > 0
        assert content.get("opendata") > 0
        assert len(content.get("catalogs")) > 0
        assert content.get("withSubject") > 0
        assert len(content.get("accessRights")) == 4
        assert len(content.get("themesAndTopicsCount")) > 0
        assert len(content.get("formats")) > 0

    @pytest.mark.integration
    def test_time_series_has_correct_format(self, client: Flask, docker_service, api):
        result = client.get("/timeseries/datasets")
        assert result.status_code == 200
        time_series = result.json
        assert time_series[0]["xAxis"] == "2020-08-01T00:00:00.000Z"
        assert time_series[0]["yAxis"] == 1251
        last_date = time_series[len(time_series) - 1]["xAxis"]
        dt = parser.parse(last_date)
        now = datetime.now()
        assert dt.month == now.month
        assert dt.year == now.year

    @pytest.mark.integration
    def test_report_filter_on_org_path(self, client: Flask, docker_service, api):
        result = client.get("/report/datasets?orgPath=/STAT/972417858/971040238")
        assert result.status_code == 200
        content = result.json
        assert content["totalObjects"] == 110
        for org in content["orgPaths"]:
            exp_orgpath_parts = "/STAT/972417858/971040238".split("/")
            for orgpath_part in org.get("key").split("/"):
                assert orgpath_part in exp_orgpath_parts

    @pytest.mark.integration
    def test_organization_id_filter(self, client: Flask, docker_service, api):
        test_org_id = "950037687"
        exp_org_path = ["/PRIVAT/950037687", "/PRIVAT"]
        result = client.get(f"/report/datasets?organizationId={test_org_id}")
        assert result.status_code == 200
        content = result.json
        assert len(content) > 0
        for orgpath in content.get("orgPaths"):
            assert orgpath["key"] in exp_org_path

    @pytest.mark.integration
    def test_theme_profile_los_path_filter(self, client: Flask, docker_service, api):
        accepted_paths = [
            "trafikk-og-transport",
            "trafikk-og-transport/mobilitetstilbud",
            "trafikk-og-transport/trafikkinformasjon",
            "trafikk-og-transport/veg-og-vegregulering",
            "trafikk-og-transport/yrkestransport",
        ]
        result = client.get("/report/datasets?themeprofile=transport")
        result_paths = result.json.get("themesAndTopicsCount")
        assert len(result_paths) > 0
        for path in result_paths:
            assert path["key"] in accepted_paths
        assert result.json.get("organizationCount") == 4
        assert result.json.get("opendata") == 20
