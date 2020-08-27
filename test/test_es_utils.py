import pytest

from src.elasticsearch.utils import add_foaf_agent_to_organization_store, add_org_and_los_paths_to_document, EsMappings
from src.organization_parser import OrganizationStore, OrganizationReferencesObject
from test.unit_mock_data import parsed_org_catalog_mock, mocked_organization_catalog_response


@pytest.fixture
def fetch_organizations_mock(mocker):
    mocker.patch('src.referenced_data_store.fetch_organizations_from_organizations_catalog',
                 return_value=mocked_organization_catalog_response)


@pytest.mark.unit
def test_add_org_path_to_document_with_dct_publisher_uri(event_loop, fetch_organizations_mock):
    result = event_loop.run_until_complete(add_org_and_los_paths_to_document(
        dct_publisher_with_national_registry["https://data.norge.no/node/2889"])
    )
    result_content = result
    assert len(result_content.keys()) == 4
    assert EsMappings.ORG_PATH in result_content.keys()
    assert result_content[EsMappings.ORG_PATH] == "/STAT/972417858/991825827"


@pytest.mark.unit
def test_add_org_path_to_document_with_foaf_agent_uri(event_loop, fetch_organizations_mock):
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = parsed_org_catalog_mock()
    event_loop.run_until_complete(add_foaf_agent_to_organization_store(agent))

    result = event_loop.run_until_complete(add_org_and_los_paths_to_document(dct_publisher_with_foaf_agent_ref["https://data.norge.no/node/2889"]))
    result_content = result
    assert len(result_content.keys()) == 4
    assert EsMappings.ORG_PATH in result_content.keys()
    assert result_content[EsMappings.ORG_PATH] == "/STAT/912660680/974760673"


@pytest.mark.unit
def test_add_to_org_store_foaf_agent(event_loop, fetch_organizations_mock):
    expected_org_path = "/STAT/912660680/974760673"
    expected_name = "Norsk Polarinstitutt"
    expected_same_as = "https://data.brreg.no/enhetsregisteret/api/enheter/974760673"
    uri = "https://register.geonorge.no/organisasjoner/norsk-polarinstitutt/201ba4f4-bb5f-4a7c-b416-de2effee5fe1"
    store_instance: OrganizationStore = OrganizationStore.get_instance()
    store_instance.organizations = parsed_org_catalog_mock()
    event_loop.run_until_complete(add_foaf_agent_to_organization_store(agent))
    assert len(store_instance.organizations) == 4
    result: OrganizationReferencesObject = store_instance.organizations[store_instance.organizations.index(uri)]
    assert result.name == expected_name
    assert result.org_path == expected_org_path
    assert result.same_as == expected_same_as


@pytest.mark.unit
def test_prepare_los_themes_without_parent():
    pass


@pytest.mark.unit
def test_prepare_los_themes_with_parent():
    pass


dct_publisher_with_national_registry = {
    "https://data.norge.no/node/2889": {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Dataset"
            }
        ],
        "http://purl.org/dc/terms/temporal": [
            {
                "type": "bnode",
                "value": "_:775b3611a97e9ab9fdc53d21ce9d1449"
            }
        ],
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827"
            }
        ]
    }
}

dct_publisher_with_foaf_agent_ref = {
    "https://data.norge.no/node/2889": {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Dataset"
            }
        ],
        "http://purl.org/dc/terms/temporal": [
            {
                "type": "bnode",
                "value": "_:775b3611a97e9ab9fdc53d21ce9d1449"
            }
        ],
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://register.geonorge.no/organisasjoner/norsk-polarinstitutt/201ba4f4-bb5f-4a7c-b416-de2effee5fe1"
            }
        ]
    }
}

agent = {
    "https://register.geonorge.no/organisasjoner/norsk-polarinstitutt/201ba4f4-bb5f-4a7c-b416-de2effee5fe1": {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/2006/vcard/ns#Kind"
            },
            {
                "type": "uri",
                "value": "http://xmlns.com/foaf/0.1/Agent"
            }
        ],
        "http://xmlns.com/foaf/0.1/mbox": [
            {
                "type": "literal",
                "value": "harvey@npolar.no"
            }
        ],
        "http://www.w3.org/2002/07/owl#sameAs": [
            {
                "type": "literal",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673"
            }
        ],
        "http://xmlns.com/foaf/0.1/name": [
            {
                "type": "literal",
                "value": "Norsk Polarinstitutt"
            }
        ],
        "http://www.w3.org/2006/vcard/ns#organization-name": [
            {
                "type": "literal",
                "value": "Norsk Polarinstitutt"
            }
        ],
        "http://purl.org/dc/terms/type": [
            {
                "type": "uri",
                "value": "http://purl.org/adms/publishertype/NationalAuthority"
            }
        ],
        "http://www.w3.org/2006/vcard/ns#hasEmail": [
            {
                "type": "uri",
                "value": "mailto:harvey@npolar.no"
            }
        ],
        "http://purl.org/dc/terms/identifier": [
            {
                "type": "literal",
                "value": "971022264"
            }
        ]
    }
}
