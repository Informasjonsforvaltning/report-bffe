from flask import Flask
import pytest


class TestDataServicesReport:
    @pytest.mark.integration
    def test_has_correct_format(self, client: Flask, docker_service, api):
        result = client.get("/report/dataservices")
        assert result.status_code == 200
        content = result.json
        keys = result.json.keys()
        assert "totalObjects" in keys
        assert "newLastWeek" in keys
        assert "orgPaths" in keys
        assert "organizationCount" in keys
        assert "formats" in keys
        assert content.get("totalObjects") > 0
        assert len(content.get("orgPaths")) > 0
        assert content.get("organizationCount") < len(content.get("orgPaths"))
        assert len(content.get("formats")) > 0

    @pytest.mark.integration
    def test_timeseries_has_correct_status(self, client: Flask, docker_service, api):
        result = client.get("/timeseries/dataservices")
        assert result.status_code == 200
