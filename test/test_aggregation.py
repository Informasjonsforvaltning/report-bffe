import pytest

from src.aggregation import create_dataset_report


@pytest.mark.unit
def test_get_datasets():
    result = create_dataset_report()


@pytest.fixture
def get_datasets_statistics_mock(mocker):
    mocker.patch('src.aggregation.get_datasets_statistics')


@pytest.fixture
def get_dataset_access_rights_mock(mocker):
    mocker.patch('src.aggregation.get_datasets_access_rights')


@pytest.fixture
def get_dataset_themes_and_topics_mock(mocker):
    mocker.patch('src.aggregation.get_datasets_themes_and_topics')
