from typing import Optional

import pytest

from fdk_reports_bff.service.service_requests import (
    fetch_all_concepts,
    fetch_dataservices,
    get_informationmodels_statistic,
)
from test.mock.dataservice_graph import dataservices
from test.unit_mock_data import concepts_response, informationmodels


@pytest.mark.unit
def test_concepts_should_perform_4_http_requests(event_loop, mock_get_xhttp_concepts):
    result = event_loop.run_until_complete(fetch_all_concepts())
    assert len(result) == 11
    assert mock_get_xhttp_concepts.call_count == 1


@pytest.fixture
def mock_get_xhttp_concepts(mocker):
    mock_values = get_xhttp_mock(status_code=200, json=concepts_response)
    return mocker.patch("httpx.AsyncClient.get", return_value=mock_values)


@pytest.mark.unit
def test_informationmodels_should_perform_http_requests(
    event_loop, mock_get_xhttp_informationmodels
):
    result = event_loop.run_until_complete(get_informationmodels_statistic())
    assert len(result) == 10
    assert mock_get_xhttp_informationmodels.call_count == 1


@pytest.fixture
def mock_get_xhttp_informationmodels(mocker):
    mock_values = get_xhttp_mock(status_code=200, json=informationmodels)
    return mocker.patch("httpx.AsyncClient.get", return_value=mock_values)


@pytest.mark.unit
def test_dataservices_should_perform_http_request(
    event_loop, mock_get_xhttp_dataservices
):
    result = event_loop.run_until_complete(fetch_dataservices())
    assert len(result) == 43
    assert mock_get_xhttp_dataservices.call_count == 1


@pytest.fixture
def mock_get_xhttp_dataservices(mocker):
    mock_values = get_xhttp_mock(status_code=200, json=dataservices)
    return mocker.patch("httpx.AsyncClient.get", return_value=mock_values)


def get_xhttp_mock(status_code, json=None):
    return MockResponse(status_code, json)


class MockResponse:
    def __init__(self, status: int = 200, json_data: Optional[dict] = None):
        self.status = (status,)
        self.json_data = json_data

    def json(self):
        return self.json_data

    def raise_for_status(self):
        return self.status
