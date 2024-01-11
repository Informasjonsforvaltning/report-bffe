from flask import Flask
import pytest


class TestConceptsReport:
    @pytest.mark.integration
    def test_get_all_update_entries(self, client: Flask, docker_service, api):
        result = client.get("/updates")
        assert result.status_code == 200

    @pytest.mark.integration
    def test_forbidden_when_missing_api_key(self, client: Flask, docker_service, api):
        result = client.post("/updates?ignore_previous=false")
        assert result.status_code == 403

    @pytest.mark.integration
    def test_updates(self, client: Flask, docker_service, api):
        result = client.post(
            "/updates?ignore_previous=false", headers={"X-API-KEY": "test-key"}
        )
        assert result.status_code == 200

    @pytest.mark.integration
    def test_updates_ignore_previous(self, client: Flask, docker_service, api):
        result = client.post(
            "/updates?ignore_previous=true", headers={"X-API-KEY": "test-key"}
        )
        assert result.status_code == 200
