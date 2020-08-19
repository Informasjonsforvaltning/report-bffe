import asyncio

import pytest

from src.dataset_aggregation import create_dataset_report
from src.responses import DataSetResponse
from test.unit_mock_data import datasets_simple_aggs_response, datasets_access_rights, datasets_themes_and_topics, \
    datasets_catalogs, datasets_format_count, parsed_org_catalog_mock, mock_access_rights_catalog_response, brreg_org


@pytest.mark.unit
def test_get_datasets(event_loop,
                      get_datasets_statistics_mock,
                      get_dataset_access_rights_mock,
                      get_dataset_themes_and_topics_mock,
                      get_dataset_catalogs_mock,
                      get_dataset_formats_mock,
                      get_organizations_mock,
                      mock_access_rights_request,
                      get_los_paths_mock,
                      get_organization_mock):
    asyncio.set_event_loop(event_loop)
    result: DataSetResponse = create_dataset_report(None, None)
    assert 8 == len(result.catalogs)
    assert 6 == len(result.formats)
    assert 76 == int(result.withSubject)
    assert 6 == int(result.opendata)
    assert 508 == int(result.totalObjects)
    assert 8 == int(result.newLastWeek)
    assert 50 == int(result.nationalComponent)
    assert 3 == len(result.accessRights)


@pytest.fixture
def get_datasets_statistics_mock(mocker):
    mocker.patch('src.dataset_aggregation.query_simple_statistic', return_value=datasets_simple_aggs_response)


@pytest.fixture
def get_dataset_access_rights_mock(mocker):
    mocker.patch('src.dataset_aggregation.get_datasets_access_rights', return_value=datasets_access_rights)


@pytest.fixture
def get_dataset_themes_and_topics_mock(mocker):
    mocker.patch('src.dataset_aggregation.get_datasets_themes_and_topics', return_value=datasets_themes_and_topics)


@pytest.fixture
def get_dataset_catalogs_mock(mocker):
    mocker.patch('src.dataset_aggregation.fetch_datasets_catalog', return_value=datasets_catalogs)


@pytest.fixture
def get_dataset_formats_mock(mocker):
    mocker.patch('src.dataset_aggregation.get_datasets_formats', return_value=datasets_format_count)


@pytest.fixture
def get_organizations_mock(mocker):
    mocker.patch('src.referenced_data_store.get_organizations', return_value=parsed_org_catalog_mock())


@pytest.fixture
def get_organization_mock(mocker):
    mocker.patch('src.referenced_data_store.get_organization_from_organization_catalog', return_value=brreg_org)


@pytest.fixture
def mock_access_rights_request(mocker):
    mocker.patch('src.referenced_data_store.fetch_access_rights_from_reference_data',
                 return_value=mock_access_rights_catalog_response())
