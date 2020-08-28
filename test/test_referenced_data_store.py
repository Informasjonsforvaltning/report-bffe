import asyncio
import pytest

from src.referenced_data_store import get_org_path, get_access_rights_code, get_los_path


@pytest.mark.unit
def test_get_org_path_in_org_catalog(event_loop, get_organizations_mock):
    result = event_loop.run_until_complete(
        get_org_path(uri="<https://data.brreg.no/enhetsregisteret/api/enheter/974760673>",
                     name="Statens Håpefulle"))
    assert result == "/STAT/912660680/974760673"


@pytest.mark.unit
def test_get_org_path_in_national_registry(get_organizations_mock, get_organization_from_service_mock, event_loop):
    result = event_loop.run_until_complete(
        get_org_path(uri="<https://data.brreg.no/enhetsregisteret/api/enheter/971040238>",
                     name="Yes ma'm"))
    assert result == "/STAT/972417858/971040238"


@pytest.mark.unit
def test_get_access_rights(event_loop, get_access_rights_mock):
    access_right_tasks = asyncio.gather(
        get_access_rights_code(
            "http://publications.europa.eu/resource/authority/access-right/RESTRICTED"),
        get_access_rights_code("http://publications.europa.eu/resource/authority/access-right/PUBLIC"),
        get_access_rights_code(
            "http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC"),
        get_access_rights_code("http://publications.europa.eu/resource/authority/access-right/NOT-A-CODE")
    )
    restricted, public, non_public, not_a_code = event_loop.run_until_complete(access_right_tasks)

    assert restricted == "RESTRICTED"
    assert public == "PUBLIC"
    assert non_public == "NON_PUBLIC"
    assert not_a_code is None


@pytest.mark.unit
def test_get_los_path(event_loop, get_los_paths_mock):
    los_path_tasks = asyncio.gather(get_los_path(["https://psi.norge.no/los/ord/festival"]),
                                    get_los_path(["https://psi.norge.no/los/ord/boligfinansiering"]))
    single_result, several_paths_result = event_loop.run_until_complete(los_path_tasks)
    assert single_result.__len__() == 1
    assert "kultur-idrett-og-fritid/kultur/festival" in single_result
    assert several_paths_result.__len__() == 2
    assert "bygg-og-eiendom/kjop-og-salg/boligfinansiering" in several_paths_result
    assert "sosiale-tjenester/okonomiske-ytelser-og-radgivning/boligfinansiering" in several_paths_result


@pytest.mark.skip
def test_get_los_path(event_loop, get_los_paths_mock):
    los_path_tasks = asyncio.gather(get_los_path(["https://psi.norge.no/los/ord/festival"]),
                                    get_los_path(["https://psi.norge.no/los/ord/boligfinansiering"]))
    single_result, several_paths_result = event_loop.run_until_complete(los_path_tasks)
    assert len(single_result[0]["losPaths"]) == 1
    assert "kultur-idrett-og-fritid/kultur/festival" in single_result[0]["losPaths"]
    assert len(several_paths_result[0]["losPaths"]) == 2
    several_paths_los_path_list = several_paths_result[0]["losPaths"]
    assert "bygg-og-eiendom/kjop-og-salg/boligfinansiering" in several_paths_los_path_list
    assert "sosiale-tjenester/okonomiske-ytelser-og-radgivning/boligfinansiering" in several_paths_los_path_list
