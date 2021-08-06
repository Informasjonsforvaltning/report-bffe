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
