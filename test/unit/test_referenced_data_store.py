import asyncio

import pytest

from fdk_reports_bff.service.referenced_data_store import (
    get_access_rights_code,
    get_los_path,
)
from test.unit_mock_data import (
    mock_los_path_reference_response,
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
