import pytest

from src.referenced_data_store import get_org_path, get_access_rights_code, get_los_path
from test.unit_mock_data import parsed_org_catalog_mock, single_parsed_org_mock, mock_access_rights_catalog_response, \
    mock_los_path_reference_response


@pytest.mark.unit
def test_get_org_path_in_org_catalog(get_organizations_mock):
    assert get_org_path("<https://data.brreg.no/enhetsregisteret/api/enheter/974760673>") == "STAT/912660680/974760673"


@pytest.mark.unit
def test_get_org_path_in_national_registry(get_organizations_mock, get_organization_from_service_mock):
    assert get_org_path("<https://data.brreg.no/enhetsregisteret/api/enheter/971040238>") == "STAT/972417858/971040238"


@pytest.mark.unit
def test_get_access_rights(get_access_rights_mock):
    assert get_access_rights_code(
        "http://publications.europa.eu/resource/authority/access-right/RESTRICTED") == "RESTRICTED"
    assert get_access_rights_code("http://publications.europa.eu/resource/authority/access-right/PUBLIC") == "PUBLIC"
    assert get_access_rights_code(
        "http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC") == "NON_PUBLIC"
    assert get_access_rights_code("http://publications.europa.eu/resource/authority/access-right/NOT-A-CODE") is None


@pytest.mark.unit
def test_get_los_path(get_los_paths_mock):
    single_result = get_los_path("https://psi.norge.no/los/ord/festival")
    assert single_result.__len__() == 1
    assert single_result.__contains__("kultur-idrett-og-fritid/kultur/festival")
    several_paths_result = get_los_path("https://psi.norge.no/los/ord/boligfinansiering")
    assert several_paths_result.__len__() == 2
    assert several_paths_result.__contains__("bygg-og-eiendom/kjop-og-salg/boligfinansiering")
    assert several_paths_result.__contains__("sosiale-tjenester/okonomiske-ytelser-og-radgivning/boligfinansiering")

@pytest.fixture
def get_organization_from_service_mock(mocker):
    mocker.patch('src.referenced_data_store.get_organization_from_service', side_effect=single_parsed_org_mock)


@pytest.fixture
def get_organizations_mock(mocker):
    mocker.patch('src.referenced_data_store.get_organizations', side_effect=parsed_org_catalog_mock)


@pytest.fixture
def get_access_rights_mock(mocker):
    mocker.patch('src.referenced_data_store.get_access_rights', side_effect=mock_access_rights_catalog_response)


@pytest.fixture
def get_los_paths_mock(mocker):
    mocker.patch('src.referenced_data_store.get_themes_and_topics_from_service',
                 side_effect=mock_los_path_reference_response)
