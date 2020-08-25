import pytest

from src.organization_parser import OrganizationStore, OrganizationReferencesObject
from test.unit_mock_data import parsed_org_catalog_mock, parsed_brreg_org, mocked_organization_catalog_response, \
    brreg_org

json_national_registry_list = [
    {
        "type": "uri",
        "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673"
    }
]
json_national_registry_list_http = [
    {
        "type": "uri",
        "value": "http://data.brreg.no/enhetsregisteret/api/enheter/974760673"
    }
]
json_national_registry_list_not_eq = [
    {
        "type": "uri",
        "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974991076"
    }
]
json_not_national_registry_list = [
    {
        "type": "uri",
        "value": "https://register.geonorge.no/organisasjoner/statistisk-sentralbyra/d4358ea8-909f-4a79-9891-c80f83f8fed3"
    }
]


@pytest.mark.unit
def test_new_organization_store():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    assert len(store_instance.organizations) == 3
    result = OrganizationStore.get_instance()
    assert result == store_instance


@pytest.mark.unit
def test_organization_store_add_organization():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    store_instance.add_organization(parsed_brreg_org)
    assert len(store_instance.organizations) == 4


@pytest.mark.unit
def test_organization_references_eq():
    national_registry_org = OrganizationReferencesObject.from_json_ld_values(
        ld_org_uri_value=json_national_registry_list)
    national_registry_org_http = OrganizationReferencesObject.from_json_ld_values(
        ld_org_uri_value=json_national_registry_list_http)
    national_registry_org_eq = OrganizationReferencesObject.from_json_ld_values(
        ld_org_uri_value=json_national_registry_list)
    national_registry_org_not_eq = OrganizationReferencesObject.from_json_ld_values(
        ld_org_uri_value=json_national_registry_list_not_eq)
    not_national_registry_org = OrganizationReferencesObject.from_json_ld_values(
        ld_org_uri_value=json_not_national_registry_list)

    assert national_registry_org == national_registry_org_eq
    assert national_registry_org == national_registry_org_http
    assert national_registry_org != not_national_registry_org
    assert national_registry_org_not_eq != national_registry_org
    assert national_registry_org == "https://data.brreg.no/enhetsregisteret/api/enheter/974760673"
    assert national_registry_org != "https://data.brreg.no/enhetsregisteret/api/enheter/9747617776"
    assert national_registry_org == "http://data.brreg.no/enhetsregisteret/api/enheter/974760673"
    assert national_registry_org == "https://data.brreg.no/enhetsregisteret/api/974760673"
    assert national_registry_org == "http://data.brreg.no/enhetsregisteret/api/974760673"
    # add same_as value for not national registry org
    not_national_registry_org.update_same_as("https://data.brreg.no/enhetsregisteret/api/enheter/974760673")
    assert national_registry_org == not_national_registry_org


@pytest.mark.unit
def test_parse_from_organization_catalog_json():
    expected = OrganizationReferencesObject(org_uri=brreg_org["norwegianRegistry"],
                                            org_path=brreg_org["orgPath"],
                                            name="STATENS KARTVERK")
    result = OrganizationReferencesObject.from_organization_catalog_single_response(brreg_org)
    assert expected == result
    assert expected == "https://data.brreg.no/enhetsregisteret/api/enheter/971040238"
    assert result.name == expected.name


@pytest.mark.unit
def test_parse_from_organization_response():
    expected = OrganizationReferencesObject(org_uri="https://data.brreg.no/enhetsregisteret/api/enheter/974760673")
    expected_1 = OrganizationReferencesObject(org_uri="https://data.brreg.no/enhetsregisteret/api/enheter/991825827")
    expected_2 = OrganizationReferencesObject(org_uri="https://data.brreg.no/enhetsregisteret/api/enheter/917422575")
    result = OrganizationReferencesObject.from_organization_catalog_list_response(mocked_organization_catalog_response)
    assert len(result) == 3
    assert expected in result
    assert expected_1 in result
    assert expected_2 in result
    assert OrganizationReferencesObject.from_json_ld_values(json_national_registry_list_http) in result
