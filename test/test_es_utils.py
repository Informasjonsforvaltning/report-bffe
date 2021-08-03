from test.unit_mock_data import mocked_organization_catalog_response

import pytest


@pytest.fixture
def fetch_organizations_mock(mocker):
    mocker.patch(
        "fdk_reports_bff.referenced_data_store.fetch_organizations_from_organizations_catalog",
        return_value=mocked_organization_catalog_response,
    )
