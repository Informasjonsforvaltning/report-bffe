import pytest
from requests import get

service_url = "http://localhost:8080"
dataservices_report_url = f"{service_url}/report/dataservices"
dataservices_timeseries_url = f"{service_url}/timeseries/dataservices"


class TestDataServicesReport:
    @pytest.mark.contract
    def test_has_correct_format(self, docker_service, api):
        result = get(url=dataservices_report_url)
        assert result.status_code == 200
        keys = result.json().keys()
        assert "totalObjects" in keys
        assert "newLastWeek" in keys
        assert "orgPaths" in keys
        assert "organizationCount" in keys
