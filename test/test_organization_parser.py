import pytest

from src.organization_parser import OrganizationStore, OrganizationReferencesObject
from test.unit_mock_data import parsed_org_catalog_mock, parsed_brreg_org, mocked_organization_catalog_response, \
    brreg_org

aas_kommune_sparql = {
    "name": {
        "type": "literal",
        "value": "Ås kommune"
    },
    "publisher": {
        "type": "uri",
        "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
    },
    "sameAs": {
        "type": "literal",
        "value": "http://data.brreg.no/enhetsregisteret/enhet/964948798"
    }
}
aas_kommune_sparql_without_publisher = {
    "name": {
        "type": "literal",
        "value": "Ås kommune"
    },
    "sameAs": {
        "type": "literal",
        "value": "http://data.brreg.no/enhetsregisteret/enhet/964948798"
    }
}
aas_kommune_sparql_without_same_as = {
    "name": {
        "type": "literal",
        "value": "Ås kommune"
    },
    "publisher": {
        "type": "uri",
        "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
    }
}
aas_kommune_organization_catalog = {
    "organizationId": "964948798",
    "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/964948798",
    "name": "ÅS KOMMUNE",
    "orgType": "KOMM",
    "orgPath": "/KOMMUNE/964948798",
    "issued": "1995-06-07",
    "municipalityNumber": "3021",
    "industryCode": "84.110",
    "sectorCode": "6500",
}
sparql_result_list = {
    "head": {
        "vars": [
            "name",
            "publisher",
            "sameAs"
        ]
    },
    "results": {
        "bindings": [
            {
                "name": {
                    "type": "literal",
                    "value": "Ås kommune"
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
                },
                "sameAs": {
                    "type": "literal",
                    "value": "http://data.brreg.no/enhetsregisteret/enhet/964948798"
                }
            },
            {
                "name": {
                    "type": "literal",
                    "value": "Avinor"
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://register.geonorge.no/organisasjoner/avinor/78ec5140-39ea-4acd-a31a-09accfa9444c"
                },
                "sameAs": {
                    "type": "literal",
                    "value": "http://data.brreg.no/enhetsregisteret/enhet/985198292"
                }
            },
            {
                "name": {
                    "type": "literal",
                    "value": "Fylkesmannsembetene"
                },
                "sameAs": {
                    "type": "literal",
                    "value": "http://data.brreg.no/enhetsregisteret/enhet/921627009"
                }
            },
            {
                "name": {
                    "type": "literal",
                    "value": "Kystverket"
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://register.geonorge.no/organisasjoner/kystverket/ceb5e459-853e-4e2f-bb22-39dc0c09cb7b"
                },
                "sameAs": {
                    "type": "literal",
                    "value": "http://data.brreg.no/enhetsregisteret/enhet/874783242"
                }
            },
            {
                "name": {
                    "type": "literal",
                    "value": "Statens vegvesen"
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://dataut.vegvesen.no/organization/e6d3dc7a-752e-418b-9afd-36533b370285"
                }
            },
            {
                "name": {
                    "type": "literal",
                    "value": "Norges geologiske undersøkelse"
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://register.geonorge.no/organisasjoner/norges-geologiske-undersokelse/d7142a92-418e-487e-a6ff-0e32c6ae31d8"
                },
                "sameAs": {
                    "type": "literal",
                    "value": "http://data.brreg.no/enhetsregisteret/enhet/970188290"
                }
            }
        ]
    }
}


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
def test_organization_store_add_sparql_result_org():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    aas_kommune = OrganizationReferencesObject.from_sparql_query_result(aas_kommune_sparql)
    store_instance.add_organization(aas_kommune)
    assert len(store_instance.organizations) == 4
    assert aas_kommune in store_instance.organizations


@pytest.mark.unit
def test_organization_store_add_sparql_result_org_with_existing_from_catalog():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    sparql_digitaliserings_direktoratet = OrganizationReferencesObject.from_sparql_query_result({
        "name": {
            "type": "literal",
            "value": "Digitaliseringsdir"
        },
        "publisher": {
            "type": "uri",
            "value": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
        }
    })
    store_instance.add_organization(sparql_digitaliserings_direktoratet)
    assert len(store_instance.organizations) == 3
    assert sparql_digitaliserings_direktoratet in store_instance.organizations


@pytest.mark.unit
def test_organization_store_add_sparql_result_org_with_same_as_in_existing_from_catalog():
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = []
    store_instance.update(organizations=parsed_org_catalog_mock())
    sparql_digitaliserings_direktoratet = OrganizationReferencesObject.from_sparql_query_result({
        "name": {
            "type": "literal",
            "value": "Digitaliseringsdir"
        },
        "publisher": {
            "type": "uri",
            "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
        },
        "sameAs": {
            "type": "uri",
            "value": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
        }
    })
    store_instance.add_organization(sparql_digitaliserings_direktoratet)
    assert len(store_instance.organizations) == 3
    assert sparql_digitaliserings_direktoratet in store_instance.organizations
    result_org = store_instance.get_organization(sparql_digitaliserings_direktoratet)
    assert result_org.org_uri == "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
    assert result_org.name == "Digitaliseringsdirektoratet"
    assert len(result_org.same_as) == 1
    assert "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a" in result_org.same_as
    result_by_orgpath = store_instance.get_organization("/STAT/972417858/991825827")
    assert result_by_orgpath == sparql_digitaliserings_direktoratet


@pytest.mark.unit
def test_sparql_references_parser():
    result = OrganizationReferencesObject.from_sparql_query_result(aas_kommune_sparql)
    assert result.name == "Ås kommune"
    assert len(result.same_as) == 1
    assert result.org_uri == "http://data.brreg.no/enhetsregisteret/enhet/964948798"
    assert result.same_as[0] == "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a" \
                                "-344191a7405a"


@pytest.mark.unit
def test_sparql_references_parser_without_same_as():
    data = {
        "name": {
            "type": "literal",
            "value": "Ås kommune"
        },
        "publisher": {
            "type": "uri",
            "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
        }
    }
    result = OrganizationReferencesObject.from_sparql_query_result(data)
    assert result.name == "Ås kommune"
    assert len(result.same_as) == 1
    assert result.same_as[0] == "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a" \
                                "-344191a7405a"
    assert result.org_uri is None


@pytest.mark.unit
def test_sparql_references_parser_without_publisher():
    data = {
        "name": {
            "type": "literal",
            "value": "Ås kommune"
        },
        "sameAs": {
            "type": "literal",
            "value": "http://data.brreg.no/enhetsregisteret/enhet/964948798"
        }
    }
    expected = OrganizationReferencesObject.from_sparql_query_result(data)
    assert expected.name == "Ås kommune"
    assert len(expected.same_as) == 0
    assert expected.org_uri == "http://data.brreg.no/enhetsregisteret/enhet/964948798"


@pytest.mark.unit
def test_parse_from_organization_catalog_json():
    expected = OrganizationReferencesObject(org_uri=brreg_org["norwegianRegistry"],
                                            org_path=brreg_org["orgPath"],
                                            name="STATENS KARTVERK")
    result = OrganizationReferencesObject.from_organization_catalog_single_response(brreg_org)
    assert expected == result
    assert expected.org_uri == "https://data.brreg.no/enhetsregisteret/api/enheter/971040238"
    assert result.name == expected.name
    assert result == "/STAT/972417858/971040238"


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


@pytest.mark.unit
def test_eq_on_org_uri():
    from_sparql_result = OrganizationReferencesObject.from_sparql_query_result(
        aas_kommune_sparql
    )
    from_sparql_result_no_publisher = OrganizationReferencesObject.from_sparql_query_result(
        aas_kommune_sparql_without_publisher
    )
    from_sparql_result_no_same_as = OrganizationReferencesObject.from_sparql_query_result(
        aas_kommune_sparql_without_same_as
    )
    from_org_catalog_json = OrganizationReferencesObject.from_organization_catalog_single_response(
        aas_kommune_organization_catalog
    )

    assert from_sparql_result == from_org_catalog_json
    assert from_sparql_result_no_publisher == from_org_catalog_json
    assert from_sparql_result_no_same_as != from_org_catalog_json


@pytest.mark.unit
def test_add_all_publishers():
    store = OrganizationStore.get_instance()
    store.organizations = []
    aas_kommune = OrganizationReferencesObject(
        name="Ås Kommune",
        org_uri="http://data.brreg.no/enhetsregisteret/enhet/964948798",
        org_path="STAT/129745/964948798"
    )
    aas_from_sparql = OrganizationReferencesObject.from_sparql_query_result(
            {
                "name": {
                    "type": "literal",
                    "value": "Ås kommune"
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://register.geonorge.no/organisasjoner/as-kommune/c084d983-080d-43b9-8c9a-344191a7405a"
                },
                "sameAs": {
                    "type": "literal",
                    "value": "http://data.brreg.no/enhetsregisteret/enhet/964948798"
                }
            }
        )
    not_in_list = OrganizationReferencesObject(
        org_uri="https://data.brreg.no/enhetsregisteret/44444448888888",
        name="not an org"
    )
    fylkesmann = OrganizationReferencesObject(
        name="Fylkesmannembetet",
        org_uri="http://data.brreg.no/enhetsregisteret/enhet/921627009"
    )
    store.add_organization(
        aas_kommune
    )

    store.add_organization(
        fylkesmann
    )
    store.add_all_publishers(sparql_result_list)
    assert len(store.organizations) == 6
    assert store.get_organization(aas_from_sparql) == aas_kommune
    assert len(aas_kommune.same_as) == 1
    assert store.get_organization(fylkesmann) is not None
    assert store.get_organization(not_in_list) is None
