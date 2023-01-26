from typing import Optional

import pytest

from fdk_reports_bff.service.service_requests import sparql_service_query
from fdk_reports_bff.sparql import get_concepts_query
from test.unit_mock_data import concepts_response


@pytest.mark.unit
def test_sparql_should_perform_1_http_request(event_loop, mock_get_xhttp_concepts):
    result = event_loop.run_until_complete(sparql_service_query(get_concepts_query()))
    assert len(result) == 11
    assert mock_get_xhttp_concepts.call_count == 1


@pytest.fixture
def mock_get_xhttp_concepts(mocker):
    mock_values = get_xhttp_mock(status_code=200, json=concepts_response)
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
