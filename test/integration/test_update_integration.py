from flask import Flask
import pytest


class TestConceptsReport:
    @pytest.mark.integration
    def test_get_all_update_entries(self, client: Flask, docker_service, api):
        result = client.get("/updates")
        assert result.status_code == 200

    @pytest.mark.integration
    def test_updates(self, client: Flask, docker_service, api):
        result = client.post("/updates?ignore_previous=false")
        assert result.status_code == 200

    @pytest.mark.integration
    def test_updates_ignore_previous(self, client: Flask, docker_service, api):
        result = client.post("/updates?ignore_previous=true")
        assert result.status_code == 200
