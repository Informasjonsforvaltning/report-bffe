import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.exceptions import MaxRetryError, NewConnectionError
from urllib3.util.retry import Retry


def wait_for_es():
    # wait  for elasticsearch to be ready
    try:
        retry_strategy = Retry(connect=2, read=5, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("http://", adapter)
        es_health = http.get(
            "http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s"
        )
        if es_health.status_code != 200:
            pytest.fail("Test containers: could not contact ElasticSearch")
    except (
        requests.exceptions.ConnectionError,
        ConnectionRefusedError,
        MaxRetryError,
        NewConnectionError,
    ):
        pytest.fail("Test containers: could not contact ElasticsSearch")
    return
