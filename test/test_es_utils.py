import pytest

from src.service_requests import fetch_catalog_from_dataset_harvester
from test.unit_mock_data import parsed_org_catalog_mock, mocked_organization_catalog_response


@pytest.fixture
def fetch_organizations_mock(mocker):
    mocker.patch('src.referenced_data_store.fetch_organizations_from_organizations_catalog',
                 return_value=mocked_organization_catalog_response)