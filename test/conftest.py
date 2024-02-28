import asyncio
import os
import time

from flask import Flask
from flask.testing import FlaskClient
import pytest
import requests

from fdk_reports_bff import create_app
from test.unit_mock_data import (
    mock_access_rights_catalog_response,
    mock_los_path_reference_response,
)
from .utils import wait_for_es

HOST_PORT = int(os.environ.get("HOST_PORT", "8080"))


def is_responsive(url):
    """Return true if response from service is 200."""
    url = f"{url}/ready"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            time.sleep(2)  # sleep extra 2 sec
            return True
    except OSError:
        return False


def start_update(url):
    response = requests.post(f"{url}/updates", headers={"X-API-KEY": "my-api-key"})
    if response.status_code != 200:
        pytest.fail(f"Unable to update, status {response.status_code}")


@pytest.fixture(scope="session")
def docker_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("fdk-reports-bff", HOST_PORT)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=90.0, pause=0.5, check=lambda: is_responsive(url)
    )
    start_update(url)
    return url


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    """Override default location of docker-compose.yml file."""
    return os.path.join(str(pytestconfig.rootdir), "./", "docker-compose.yml")


@pytest.fixture(scope="session")
def api():
    wait_for_es()
    yield


@pytest.mark.integration
@pytest.fixture
def app():
    """Returns a Flask app for integration testing."""
    app = create_app({})
    yield app


@pytest.mark.integration
@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Returns a client for integration testing."""
    return app.test_client()


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture
def get_access_rights_mock(mocker):
    mocker.patch(
        "fdk_reports_bff.service.referenced_data_store.fetch_access_rights_from_reference_data",
        side_effect=mock_access_rights_catalog_response,
    )


@pytest.fixture
def get_los_paths_mock(mocker):
    mocker.patch(
        "fdk_reports_bff.service.referenced_data_store.fetch_themes_and_topics_from_reference_data",
        side_effect=mock_los_path_reference_response,
    )
