from datetime import datetime

import pytest
from requests import get

service_url = "http://localhost:8000"
dataset_report_url = f"{service_url}/report/datasets"
dataset_time_series_url = f"{service_url}/timeseries/datasets"


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
    def test_timeseries_has_correct_format(self, wait_for_ready):
        result = get(url=dataset_time_series_url)
        assert result.status_code == 200
        time_series = result.json()
        assert time_series[0]["xAxis"] == "01.09.2011"
        assert time_series[0]["yAxis"] == "12"
        last_date = time_series[len(time_series)-1]["xAxis"]
        dt = datetime.strptime(last_date, '%d.%m.%Y')
        now = datetime.now()
        assert dt.month == now.month
        assert dt.year == now.year