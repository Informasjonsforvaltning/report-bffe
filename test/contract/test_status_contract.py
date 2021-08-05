import pytest
from requests import get

service_url = "http://localhost:8080"


class TestConceptsReport:
    @pytest.mark.contract
    def test_ping(self, docker_service, api):
        result = get(url=f"{service_url}/ping")
        assert result.status_code == 200

    @pytest.mark.contract
    def test_ready(self, docker_service, api):
        result = get(url=f"{service_url}/ready")
        assert result.status_code == 200
