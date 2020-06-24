import pytest

from src.organization_parser import ParsedOrganization


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
