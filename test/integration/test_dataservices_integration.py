from flask import Flask
import pytest


class TestDataServicesReport:
    @pytest.mark.integration
    def test_has_correct_format(self, client: Flask, docker_service, api):
        result = client.get("/report/dataservices")
        assert result.status_code == 200
        keys = result.json.keys()
        assert "totalObjects" in keys
        assert "newLastWeek" in keys
        assert "orgPaths" in keys
        assert "organizationCount" in keys

    @pytest.mark.integration
    def test_timeseries_has_correct_status(self, client: Flask, docker_service, api):
        result = client.get("/timeseries/dataservices")
        assert result.status_code == 200
