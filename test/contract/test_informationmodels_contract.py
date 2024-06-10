import pytest
from requests import get

service_url = "http://localhost:8080"
informationmodels_report_url = f"{service_url}/report/informationmodels"
informationmodels_timeseries_url = f"{service_url}/timeseries/informationmodels"


class TestInformationModelsReport:
    @pytest.mark.contract
    def test_has_correct_format(self, docker_service, api):
        result = get(url=informationmodels_report_url)
        assert result.status_code == 200
        keys = result.json().keys()
        assert "totalObjects" in keys
        assert "newLastWeek" in keys
        assert "orgPaths" in keys
        assert "organizationCount" in keys
