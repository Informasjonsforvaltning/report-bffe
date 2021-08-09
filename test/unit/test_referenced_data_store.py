import asyncio

import pytest

from fdk_reports_bff.referenced_data_store import (
    get_access_rights_code,
    get_los_path,
    get_open_licenses,
    OpenLicense,
)
from test.unit_mock_data import (
    mock_los_path_reference_response,
    open_licenses_mock_reponse,
)


@pytest.mark.unit
def test_get_access_rights(event_loop, get_access_rights_mock):
    access_right_tasks = asyncio.gather(
        get_access_rights_code(
            "http://publications.europa.eu/resource/authority/access-right/RESTRICTED"
        ),
        get_access_rights_code(
            "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
        ),
        get_access_rights_code(
            "http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC"
        ),
        get_access_rights_code(
            "http://publications.europa.eu/resource/authority/access-right/NOT-A-CODE"
        ),
    )
    restricted, public, non_public, not_a_code = event_loop.run_until_complete(
        access_right_tasks
    )

    assert restricted == "RESTRICTED"
    assert public == "PUBLIC"
    assert non_public == "NON_PUBLIC"
    assert not_a_code is None


@pytest.mark.unit
def test_get_safe_base_uri_for_open_license():
    expected_result = "creativecommons.org/licenses/by/4.0"
    assert (
        OpenLicense.get_base_uri("http://creativecommons.org/licenses/by/4.0/")
        == expected_result
    )
    assert (
        OpenLicense.get_base_uri("https://creativecommons.org/licenses/by/4.0/")
        == expected_result
    )
    assert (
        OpenLicense.get_base_uri("https://creativecommons.org/licenses/by/4.0")
        == expected_result
    )


@pytest.mark.unit
def test_get_open_licenses(event_loop, fetch_open_licenses_mock):
    result = event_loop.run_until_complete(get_open_licenses())
    assert len(result) == 7
    assert "http://creativecommons.org/licenses/by/4.0/" in result
    assert "https://creativecommons.org/licenses/by/4.0/" in result
    assert "http://creativecommons.org/licenses/by/4.0" in result
    assert "http://creativecommons.org/licenses/by/4.0/deed.no" in result
    assert "http://creativecommons.org/licenses/by/4.0/deed.no/" in result
    assert "http://creativecommons.org/licenses/by/4.0/deed" not in result


@pytest.mark.unit
def test_get_los_path():
    los_paths = mock_los_path_reference_response()
    single_result = get_los_path(["https://psi.norge.no/los/ord/festival"], los_paths)
    several_paths_result = get_los_path(
        ["https://psi.norge.no/los/ord/boligfinansiering"], los_paths
    )
    assert single_result.__len__() == 1
    assert "kultur-idrett-og-fritid/kultur/festival" in single_result
    assert several_paths_result.__len__() == 2
    assert "bygg-og-eiendom/kjop-og-salg/boligfinansiering" in several_paths_result
    assert (
        "sosiale-tjenester/okonomiske-ytelser-og-radgivning/boligfinansiering"
        in several_paths_result
    )


@pytest.fixture
def fetch_open_licenses_mock(mocker):
    mocker.patch(
        "fdk_reports_bff.referenced_data_store.fetch_open_licences_from_reference_data",
        side_effect=open_licenses_mock_reponse,
    )
