import pytest
from requests import get

service_url = "http://localhost:8000"
dataset_report_url = f"{service_url}/report/datasets"


class TestDatasetsReport:

    @pytest.mark.contract
    def test_has_correct_format(self, wait_for_ready):
        result = get(url=dataset_report_url)
        assert result.status_code == 200
        keys = result.json().keys()
        assert "totalObjects" in keys
        assert "newLastWeek" in keys
        assert "nationalComponent" in keys
        assert "opendata" in keys
        assert "catalogs" in keys
        assert "withSubject" in keys
        assert "accessRights" in keys
        assert "themesAndTopicsCount" in keys

    @pytest.mark.contract
    def test_report_has_correct_format(self, wait_for_ready):
        result = get(url=dataset_report_url)
        assert result.status_code == 200
        keys = result.json().keys()
        assert "totalObjects" in keys
        assert "newLastWeek" in keys
        assert "nationalComponent" in keys
        assert "opendata" in keys
        assert "catalogs" in keys
        assert "withSubject" in keys
        assert "accessRights" in keys
        assert "themesAndTopicsCount" in keys

