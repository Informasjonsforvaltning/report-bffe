import pytest

from src.organization_parser import ParsedOrganization, OrganizationStore
from test.unit_mock_data import parsed_org_catalog_mock, brreg_org

unknown_org: ParsedOrganization = ParsedOrganization(uri="http://someone.did.it.wrong/nkala", name="Just not right")
unknown_org.dataset_reference_uri = "http://someone.did.it.wrong/nkala"
other_org: ParsedOrganization = ParsedOrganization(uri="http://someone.did.it.wrong/nhiasoi", name="Another made wrong")
other_org.dataset_reference_uri = "http://someone.did.it.wrong/nhiasoi"

@pytest.mark.unit
def test_is_national_registry_uri():
    assert ParsedOrganization.is_national_registry_uri("https://data.brreg.no/enhetsregisteret/api/enheter/971040238")
    assert ParsedOrganization.is_national_registry_uri("http://data.brreg.no/enhetsregisteret/api/enheter/971040238")
    assert ParsedOrganization.is_national_registry_uri("http://data.brreg.no/enhetsregisteret/enheter/971040238")
    assert ParsedOrganization.is_national_registry_uri("https://data.brreg.no/enhetsregisteret/api/enheter/971040238")

    assert not ParsedOrganization.is_national_registry_uri("https://data.no/enhetsregisteret/api/enheter/971040238")
    assert not ParsedOrganization.is_national_registry_uri("http://data.brreg.no/api/enheter/971040238")
    assert not ParsedOrganization.is_national_registry_uri("http://data.brreg.no/enhetsregis/enheter/971040238")
    assert not ParsedOrganization.is_national_registry_uri("https://enhetsregisteret/api/enheter/971040238")


@pytest.mark.unit
def test_resolve_id():
    assert not ParsedOrganization.resolve_id(uri=None, org_id=None)
    assert ParsedOrganization.resolve_id(uri=None, org_id="1234568781") == "1234568781"
    assert ParsedOrganization.resolve_id(uri=None, org_id="12345hh88")
    assert ParsedOrganization.resolve_id(
        uri="https://data.brreg.no/enhetsregisteret/api/enheter/971040238") == "971040238"
    assert not ParsedOrganization.resolve_id(uri="https://data.brreg.no/et/api/enheter/971040238")


@pytest.mark.unit
def test_eq():
    org_name_some_name = ParsedOrganization(name="Some Name")
    org_national_reg_971040238_some_name = ParsedOrganization(name="Some Name",
                                                              uri="https://data.brreg.no/enhetsregisteret/api/enheter"
                                                                  "/971040238")
    org_national_reg_971040238_other_name = ParsedOrganization(name="Other Name",
                                                               uri="https://data.brreg.no/enhetsregisteret/api"
                                                                   "/enheter/971040238")
    org_not_national_reg_971040238_some_name = ParsedOrganization(name="Some Name",
                                                                  uri="https://dat.no/enhetsregisteret/api/enheter/971040238")
    org_not_national_reg_971040238_other_name = ParsedOrganization(name="Other Name",
                                                                   uri="https://dat.no/enhetsregisteret/api/enheter/971040238")
    org_with_id_971040238_some_name = ParsedOrganization(name="Some Name", org_id="971040238")
    org_with_id_971040238_other_name = ParsedOrganization(name="Name, name", org_id="971040238")
    org_with_id_971040555_some_name = ParsedOrganization(name="Some Name", org_id="971040555")
    assert org_name_some_name == "Some Name"
    assert org_name_some_name != "Other Name"
    assert org_name_some_name == org_national_reg_971040238_some_name
    assert org_name_some_name != org_national_reg_971040238_other_name
    assert org_name_some_name == org_with_id_971040238_some_name
    assert org_name_some_name != org_with_id_971040238_other_name
    assert org_name_some_name == org_not_national_reg_971040238_some_name
    assert org_name_some_name != org_not_national_reg_971040238_other_name
    assert org_name_some_name == org_with_id_971040555_some_name
    assert org_with_id_971040238_other_name == org_national_reg_971040238_some_name
    assert org_national_reg_971040238_some_name == org_with_id_971040238_some_name
    assert org_national_reg_971040238_some_name == org_with_id_971040238_other_name
    assert org_not_national_reg_971040238_other_name != org_national_reg_971040238_some_name
    assert org_not_national_reg_971040238_other_name == org_not_national_reg_971040238_other_name


@pytest.mark.unit
def test_eq_org_path():
    org_path_from_catalog = ParsedOrganization.from_organizations_catalog_json({
        "organizationId": "974760673",
        "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673",
        "name": "REGISTERENHETEN I BRØNNØYSUND",
        "orgType": "ORGL",
        "orgPath": "STAT/912660680/974760673",
        "subOrganizationOf": "912660680",
        "issued": "1995-08-09",
        "municipalityNumber": "1813",
        "industryCode": "84.110",
        "sectorCode": "6100"
    })

    assert org_path_from_catalog == ['STAT']
    assert org_path_from_catalog == ['STAT', '912660680']
    assert org_path_from_catalog == ['STAT', '912660680', '974760673']
    assert org_path_from_catalog != ['STAT', '912660681']
    assert org_path_from_catalog != ['STAT', '92660681']
    assert org_path_from_catalog != ['STAT', '912660680', '974760673', '776655']


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
    store_instance.add_organization(brreg_org)
    assert len(store_instance.organizations) == 4

    store_instance.add_organization(unknown_org)
    assert len(store_instance.organizations) == 5
    store_instance.add_organization(unknown_org)
    store_instance.add_organization(brreg_org)
    store_instance.add_organization(unknown_org)
    store_instance.add_organization(brreg_org)
    store_instance.add_organization(other_org)
    assert len(store_instance.organizations) == 6

@pytest.mark.unit
def test_get_dataset_reference_by_org_path():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    org_catalog_mock = parsed_org_catalog_mock()
    org_catalog_mock.append(brreg_org)
    for org in org_catalog_mock:
        org.dataset_reference_uri = org.uri
    store_instance.update(organizations=org_catalog_mock)
    store_instance.add_organization(unknown_org)
    store_instance.add_organization(brreg_org)

    unknown_org_result = store_instance.get_dataset_reference_for_orgpath(
        unknown_org.orgPath)
    assert len(unknown_org_result) == 1
    assert unknown_org_result[0] == "http://someone.did.it.wrong/nkala"
    org_catalog_org_1 = store_instance.get_dataset_reference_for_orgpath(orgpath="/STAT/912660680/974760673")
    assert len(org_catalog_org_1) == 1
    partial_org_path = store_instance.get_dataset_reference_for_orgpath(orgpath="/STAT/972417858")
    assert len(partial_org_path) == 2




