import pytest

from src.organization_parser import ParsedOrganization, OrganizationStore
from src.utils import BadOrgPathException
from test.unit_mock_data import parsed_org_catalog_mock

brreg_org: ParsedOrganization = ParsedOrganization.from_organizations_catalog_json({
    "organizationId": "971040238",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/971040238",
    "name": "STATENS KARTVERK",
    "orgType": "ORGL",
    "orgPath": "STAT/972417858/971040238",
    "subOrganizationOf": "972417858",
    "issued": "1995-03-12",
    "municipalityNumber": "3007",
    "industryCode": "71.123",
    "sectorCode": "6100"
}
)
unknown_org: ParsedOrganization = ParsedOrganization(uri="http://someone.did.it.wrong/nkala", name="Just not right")
other_org: ParsedOrganization = ParsedOrganization(uri="http://someone.did.it.wrong/nhiasoi", name="Another made wrong")


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
                                                              uri="https://data.brreg.no/enhetsregisteret/api/enheter/971040238")
    org_national_reg_971040238_other_name = ParsedOrganization(name="Other Name",
                                                               uri="https://data.brreg.no/enhetsregisteret/api/enheter/971040238")
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
def test_eq_old_org_path():
    org_path_from_catalog = ParsedOrganization.from_organizations_catalog_json({
        "organizationId": "974760673",
        "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673",
        "name": "REGISTERENHETEN I BRØNNØYSUND",
        "orgType": "ORGL",
        "orgPath": "/STAT/912660680/974760673",
        "subOrganizationOf": "912660680",
        "issued": "1995-08-09",
        "municipalityNumber": "1813",
        "industryCode": "84.110",
        "sectorCode": "6100"
    })

    assert org_path_from_catalog == ['STAT']
    assert org_path_from_catalog == ['STAT', '912660680']
    assert org_path_from_catalog != ['STAT', '912660681']
    assert org_path_from_catalog != ['STAT', '912660680', '974760673']
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
def test_organization_store_update_should_retain_retain_unknown_organizations():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    store_instance.add_organization(brreg_org)
    store_instance.add_organization(unknown_org)
    # second update
    update_with = ParsedOrganization.parse_list([
        {
            "organizationId": "55555555",
            "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/55555555",
            "internationalRegistry": None,
            "name": "Digitaliseringsdirektoratet",
            "orgType": "ORGL",
            "orgPath": "STAT/972417858/55555555",
            "subOrganizationOf": "972417858",
            "issued": "2007-10-15",
            "municipalityNumber": "0301",
            "industryCode": "84.110",
            "sectorCode": "6100",
            "prefLabel": {
                "nb": "Digitaliseringsdirektoratet",
                "nn": "Digitaliseringsdirektoratet",
                "en": "Norwegian Digitalisation Agency"
            },
            "allowDelegatedRegistration": None
        },
        {
            "organizationId": "44444444",
            "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/44444444",
            "internationalRegistry": None,
            "name": "ENTUR AS",
            "orgType": "AS",
            "orgPath": "PRIVAT/44444444",
            "subOrganizationOf": None,
            "issued": "2016-07-04",
            "municipalityNumber": "0301",
            "industryCode": "62.010",
            "sectorCode": "1120",
            "prefLabel": None,
            "allowDelegatedRegistration": None
        }])

    store_instance.update(update_with)
    assert len(store_instance.organizations) == 3
    assert unknown_org in store_instance.organizations
    assert update_with[0] in store_instance.organizations
    assert update_with[1] in store_instance.organizations
    assert brreg_org not in store_instance.organizations


@pytest.mark.unit
def test_get_organization_by_org_path():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    store_instance.add_organization(unknown_org)
    store_instance.add_organization(brreg_org)
    unknown_org_result = store_instance.get_organization_uris_from_org_path(
        unknown_org.orgPath)
    assert len(unknown_org_result) == 1
    assert unknown_org_result[0] == "http://someone.did.it.wrong/nkala"
    assert store_instance.get_organization_uris_from_org_path(
        brreg_org.orgPath)[0] == "https://data.brreg.no/enhetsregisteret/api/enheter/971040238"
    assert store_instance.get_organization_uris_from_org_path(
        "STAT/912660680/974760673")[0] == "https://data.brreg.no/enhetsregisteret/api/enheter/974760673"
    assert len(store_instance.get_organization_uris_from_org_path("STAT")) == 3
    assert len(store_instance.get_organization_uris_from_org_path("STAT/972417858")) == 2
    with pytest.raises(BadOrgPathException):
        store_instance.get_organization_uris_from_org_path("PRIVAT/1235779999/7777")





# NB! må håndtere organisasjoner utenfor enhetsregisteret
