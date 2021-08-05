from flask import Flask
import pytest


class TestConceptsReport:
    @pytest.mark.integration
    def test_ping(self, client: Flask, docker_service, api):
        result = client.get("/ping")
        assert result.status_code == 200

    @pytest.mark.integration
    def test_ready(self, client: Flask, docker_service, api):
        result = client.get("/ready")
        assert result.status_code == 200
