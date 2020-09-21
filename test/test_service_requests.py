import pytest

from src.elasticsearch.concepts import insert_concepts
from src.service_requests import fetch_all_concepts
from test.unit_mock_data import concepts_response


@pytest.mark.unit
def test_concepts_should_perform_4_http_requests(event_loop, mock_get_xhttp_concepts):
    result = event_loop.run_until_complete(fetch_all_concepts())
    assert len(result) == 20
    assert mock_get_xhttp_concepts.call_count == 4
    number_counts = [x[1]['params']['page'] for x in mock_get_xhttp_concepts.await_args_list]
    assert 0 in number_counts
    assert 1 in number_counts
    assert 2 in number_counts
    assert 3 in number_counts


def test_dry_run(mocker):
    mocker.patch('os.getcwd', return_value='/Users/bbreg/Documents/fdk-reports-bff')
    insert_concepts()


@pytest.fixture
def mock_get_xhttp_concepts(mocker):
    mock_values = get_xhttp_mock(status_code=200, json=concepts_response)
    return mocker.patch('httpx.AsyncClient.get',
                        return_value=mock_values
                        )


def get_xhttp_mock(status_code, json=None):
    return MockResponse(status_code, json)


class MockResponse:
    def __init__(self, status: int = 200, json_data: dict = None):
        self.status = status,
        self.json_data = json_data

    def json(self):
        return self.json_data
