import pytest

from src.elasticsearch.rdf_reference_mappers import CatalogReference, RdfReferenceMapper, CatalogRecords
from src.rdf_namespaces import JSON_RDF
from src.utils import ContentKeys
from src.referenced_data_store import OpenLicense


@pytest.mark.unit
def test_catalog_reference_without_datasets():
    rdf_catalog = ("http://registration-api:8080/catalogs/911259583", {
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/911259583"
            }
        ],
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Catalog"
            }
        ],
        "http://purl.org/dc/terms/title": [
            {
                "type": "literal",
                "value": "Datakatalog for VÅLER I ØSTFOLD OG VIKHAMMER",
                "lang": "nb"
            }
        ]
    })
    records = [CatalogRecords(entry) for entry in mock_records]
    result = CatalogReference(catalog_entry=rdf_catalog, catalog_records=records)
    assert result.name == "Datakatalog for VÅLER I ØSTFOLD OG VIKHAMMER"
    assert result.uri == "http://registration-api:8080/catalogs/911259583"
    assert len(result.datasets) == 0


@pytest.mark.unit
def test_catalog_reference_with_datasets():
    rdf_catalog = ("http://registration-api:8080/catalogs/911259583", {
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/911259583"
            }
        ],
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Catalog"
            }
        ],
        "http://purl.org/dc/terms/title": [
            {
                "type": "literal",
                "value": "Datakatalog for VÅLER I ØSTFOLD OG VIKHAMMER",
                "lang": "nb"
            }
        ],
        "http://www.w3.org/ns/dcat#dataset": [
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/ebd0aa41-da69-4f37-a44a-2d10f127a68a"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/3749f2c6-0d16-4bfb-b74f-6597b3705e2e"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/c6b9e443-12a4-4d29-854a-0f6eda682858"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/a4c9556f-9874-400b-80ad-7cd74cfb3c23"
            }]
    })
    records = [CatalogRecords(entry) for entry in mock_records]
    result = CatalogReference(catalog_entry=rdf_catalog, catalog_records=records)
    assert result.name == "Datakatalog for VÅLER I ØSTFOLD OG VIKHAMMER"
    assert result.uri == "http://registration-api:8080/catalogs/911259583"
    assert len(result.datasets) == 4
    assert "http://brreg.no/catalogs/910244132/datasets/ebd0aa41-da69-4f37-a44a-2d10f127a68a" in result.datasets
    assert "http://brreg.no/catalogs/910244132/datasets/3749f2c6-0d16-4bfb-b74f-6597b3705e2e" in result.datasets
    assert "http://brreg.no/catalogs/910244132/datasets/c6b9e443-12a4-4d29-854a-0f6eda682858" in result.datasets
    assert "http://brreg.no/catalogs/910244132/datasets/a4c9556f-9874-400b-80ad-7cd74cfb3c23" in result.datasets


@pytest.mark.unit
def test_catalog_reference_eq_on_uri():
    rdf_catalog = ("http://registration-api:8080/catalogs/911259583", {
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/911259583"
            }
        ],
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Catalog"
            }
        ],
        "http://purl.org/dc/terms/title": [
            {
                "type": "literal",
                "value": "Datakatalog for VÅLER I ØSTFOLD OG VIKHAMMER",
                "lang": "nb"
            }
        ],
        "http://www.w3.org/ns/dcat#dataset": [
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/ebd0aa41-da69-4f37-a44a-2d10f127a68a"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/3749f2c6-0d16-4bfb-b74f-6597b3705e2e"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/c6b9e443-12a4-4d29-854a-0f6eda682858"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/a4c9556f-9874-400b-80ad-7cd74cfb3c23"
            }]
    })
    records = [CatalogRecords(entry) for entry in mock_records]
    result = CatalogReference(catalog_entry=rdf_catalog, catalog_records=records)
    assert result == "http://registration-api:8080/catalogs/911259583"


@pytest.mark.unit
def test_catalog_reference_eq_on_catalog_record_entry():
    rdf_catalog = ("http://registration-api:8080/catalogs/911527170", {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Catalog"
            }
        ],
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/911527170"
            }
        ],
        "http://www.w3.org/ns/dcat#dataset": [
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/911527170/datasets/ef06c5b3-c440-4948-9189-c03de9b4c52b"
            }
        ],
        "http://purl.org/dc/terms/title": [
            {
                "type": "literal",
                "value": "Datakatalog for SKATVAL OG BREIVIKBOTN",
                "lang": "nb"
            }
        ]
    })
    ref_records = [
        CatalogRecords(
            record_entry=(
                "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/c554d078-c583-395d-b7c1-950a1f287c33",
                {
                    "http://purl.org/dc/terms/issued": [
                        {
                            "type": "literal",
                            "value": "2020-08-19T09:39:37.919Z",
                            "datatype": "http://www.w3.org/2001/XMLSchema#dateTime"
                        }
                    ],
                    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                        {
                            "type": "uri",
                            "value": "http://www.w3.org/ns/dcat#CatalogRecord"
                        }
                    ],
                    "http://xmlns.com/foaf/0.1/primaryTopic": [
                        {
                            "type": "uri",
                            "value": "http://registration-api:8080/catalogs/911527170"
                        }
                    ],
                    "http://purl.org/dc/terms/modified": [
                        {
                            "type": "literal",
                            "value": "2020-08-19T09:39:37.919Z",
                            "datatype": "http://www.w3.org/2001/XMLSchema#dateTime"
                        }
                    ],
                    "http://purl.org/dc/terms/identifier": [
                        {
                            "type": "literal",
                            "value": "c554d078-c583-395d-b7c1-950a1f287c33"
                        }
                    ]
                })),
        CatalogRecords(
            record_entry=mock_records[1]
        )
    ]
    result = CatalogReference(
        catalog_entry=rdf_catalog,
        catalog_records=ref_records
    )
    assert len(result.record_refs) == 1
    assert result == "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/c554d078-c583-395d-b7c1" \
                     "-950a1f287c33 "


@pytest.mark.unit
def test_catalog_reference_eq_on_dataset_uri():
    rdf_catalog = ("http://registration-api:8080/catalogs/911259583", {
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/911259583"
            }
        ],
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Catalog"
            }
        ],
        "http://purl.org/dc/terms/title": [
            {
                "type": "literal",
                "value": "Datakatalog for VÅLER I ØSTFOLD OG VIKHAMMER",
                "lang": "nb"
            }
        ],
        "http://www.w3.org/ns/dcat#dataset": [
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/ebd0aa41-da69-4f37-a44a-2d10f127a68a"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/3749f2c6-0d16-4bfb-b74f-6597b3705e2e"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/c6b9e443-12a4-4d29-854a-0f6eda682858"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/a4c9556f-9874-400b-80ad-7cd74cfb3c23"
            }]
    })
    records = [CatalogRecords(entry) for entry in mock_records]
    result = CatalogReference(catalog_entry=rdf_catalog, catalog_records=records)
    assert result == "http://registration-api:8080/catalogs/911259583"
    assert "http://brreg.no/catalogs/910244132/datasets/ebd0aa41-da69-4f37-a44a-2d10f127a68a" == result
    assert "http://brreg.no/catalogs/910244132/datasets/3749f2c6-0d16-4bfb-b74f-6597b3705e2e" == result
    assert "http://brreg.no/catalogs/910244132/datasets/c6b9e443-12a4-4d29-854a-0f6eda682858" == result
    assert "http://brreg.no/catalogs/910244132/datasets/a4c9556f-9874-400b-80ad-7cd74cfb3c23" == result


@pytest.mark.unit
def test_reference_mapper_for_catalogs(empty_open_licence_b_nodes_patch):
    result = RdfReferenceMapper(
        document_list=mock_records + mock_catalogs + mock_datasets + mock_distributions + mock_licence_documents,
        open_licenses=mock_open_licenses,
        media_types=[]
    )

    assert len(result.catalogs) == 4
    assert len(result.catalog_records) == 4
    for entry in result.catalogs:
        assert type(entry) is CatalogReference
    assert result.get_dataset_catalog_name(
        dataset_node_uri="http://brreg.no/catalogs/910244132/datasets/85875858585858a") == "Datakatalog for VÅLER I ØSTFOLD OG VIKHAMMER"
    assert result.get_dataset_catalog_name(
        record_part_of_uri="http://registration-api:8080/catalogs/876543231") == "Datakatalog without dcat dataset"
    assert result.get_dataset_catalog_name(
        dataset_node_uri="http://brreg.no/catalogs/910244132/datasets/3749f2c6-0d16-4bfb-b74f-6597b3705e2e") == "Datakatalog with dcat dataset"
    assert result.get_dataset_catalog_name(
        "http://brreg.no/catalogs/910244132/datasets/3749f2c6-0d16-4bfbnotinlist3705e2e") is None


@pytest.mark.unit
def test_get_record_for_dataset(empty_open_licence_b_nodes_patch):
    mapper = RdfReferenceMapper(
        document_list=mock_records + mock_catalogs + mock_datasets + mock_distributions + mock_licence_documents,
        open_licenses=mock_open_licenses,
        media_types=[]
    )

    result = mapper.get_catalog_record_for_dataset(dataset_uri="https://data.norge.no/node/1589")
    result_keys = result.keys()
    assert JSON_RDF.dct.issued in result_keys
    assert JSON_RDF.dct.isPartOf in result_keys
    assert JSON_RDF.foaf.primaryTopic in result_keys
    assert result[JSON_RDF.dct.isPartOf][0][
               ContentKeys.VALUE] == "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/a4153a19-50f9-332b-b7ae-fe3273cbada7"
    assert result[JSON_RDF.foaf.primaryTopic][0][ContentKeys.VALUE] == "https://data.norge.no/node/1589"
    assert result[JSON_RDF.dct.issued][0][ContentKeys.VALUE] == '2020-08-19T09:39:29.822Z'
    exp_no_result = mapper.get_catalog_record_for_dataset(dataset_uri="https://data.norge.no/node/99887766")
    assert exp_no_result is None


@pytest.fixture
def empty_open_licence_b_nodes_patch(mocker):
    mocker.patch("src.elasticsearch.rdf_reference_mappers.RdfReferenceMapper.get_open_license_nodes_from_license_docs",
                 return_value=[])


mock_records = [
    ('https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b827ea5e-912a-362a-abfc-ba06fe1cb77f', {
        'http://purl.org/dc/terms/issued': [{'type': 'literal', 'value': '2020-08-19T09:39:29.822Z',
                                             'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime'}],
        'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
            {'type': 'uri', 'value': 'http://www.w3.org/ns/dcat#CatalogRecord'}],
        'http://purl.org/dc/terms/isPartOf': [
            {'type': 'uri',
             'value':
                 'https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/a4153a19-50f9-332b-b7ae-fe3273cbada7'}],
        'http://xmlns.com/foaf/0.1/primaryTopic': [{'type': 'uri', 'value': 'https://data.norge.no/node/1589'}],
        'http://purl.org/dc/terms/modified': [{'type': 'literal', 'value': '2020-08-19T09:39:29.822Z',
                                               'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime'}],
        'http://purl.org/dc/terms/identifier': [{'type': 'literal', 'value': 'b827ea5e-912a-362a-abfc-ba06fe1cb77f'}]}),
    ('https://datasets.staging.fellesdatakatalog.digdir.no/datasets/45a5965e-e3a9-32ec-8e99-695017c10140', {
        'http://purl.org/dc/terms/issued': [{'type': 'literal', 'value': '2020-08-19T09:39:29.822Z',
                                             'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime'}],
        'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
            {'type': 'uri', 'value': 'http://www.w3.org/ns/dcat#CatalogRecord'}],
        'http://purl.org/dc/terms/isPartOf': [{'type': 'uri',
                                               'value': 'https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/a4153a19-50f9-332b-b7ae-fe3273cbada7'}],
        'http://xmlns.com/foaf/0.1/primaryTopic': [{'type': 'uri', 'value': 'https://data.norge.no/node/844'}],
        'http://purl.org/dc/terms/modified': [{'type': 'literal', 'value': '2020-08-19T09:39:29.822Z',
                                               'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime'}],
        'http://purl.org/dc/terms/identifier': [
            {'type': 'literal', 'value': '45a5965e-e3a9-32ec-8e99-695017c10140'}]}),
    ('https://datasets.staging.fellesdatakatalog.digdir.no/datasets/76e45d64-b4fc-39a7-a77d-17804d97ac96', {
        'http://purl.org/dc/terms/issued': [{'type': 'literal', 'value': '2020-08-19T09:39:29.822Z',
                                             'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime'}],
        'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
            {'type': 'uri', 'value': 'http://www.w3.org/ns/dcat#CatalogRecord'}],
        'http://purl.org/dc/terms/isPartOf': [{'type': 'uri',
                                               'value': 'https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/a4153a19-50f9-332b-b7ae-fe3273cbada7'}],
        'http://xmlns.com/foaf/0.1/primaryTopic': [{'type': 'uri', 'value': 'https://data.norge.no/node/3153'}],
        'http://purl.org/dc/terms/modified': [{'type': 'literal', 'value': '2020-08-19T09:39:29.822Z',
                                               'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime'}],
        'http://purl.org/dc/terms/identifier': [
            {'type': 'literal', 'value': '76e45d64-b4fc-39a7-a77d-17804d97ac96'}]}),
    ("https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/c554d078-c583-395d-b7c1-950a1f287c33", {
        "http://purl.org/dc/terms/issued": [
            {
                "type": "literal",
                "value": "2020-08-19T09:39:37.919Z",
                "datatype": "http://www.w3.org/2001/XMLSchema#dateTime"
            }
        ],
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#CatalogRecord"
            }
        ],
        "http://xmlns.com/foaf/0.1/primaryTopic": [
            {
                "type": "uri",
                "value": "http://registration-api:8080/catalogs/911527170"
            }
        ],
        "http://purl.org/dc/terms/modified": [
            {
                "type": "literal",
                "value": "2020-08-19T09:39:37.919Z",
                "datatype": "http://www.w3.org/2001/XMLSchema#dateTime"
            }
        ],
        "http://purl.org/dc/terms/identifier": [
            {
                "type": "literal",
                "value": "c554d078-c583-395d-b7c1-950a1f287c33"
            }
        ]
    })
]
mock_datasets = [
    ('https://kartkatalog.geonorge.no/Metadata/uuid/5857ec0a-8d2c-4cd8-baa2-0dc54ae213b4',
     {'http://purl.org/dc/terms/spatial': [{'type': 'bnode', 'value': '_:b1bc8ab54b2d650fa9998dc6f9670bba'}],
      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
          {'type': 'uri', 'value': 'http://www.w3.org/ns/dcat#Dataset'}], 'http://xmlns.com/foaf/0.1/thumbnail': [
         {'type': 'uri',
          'value': 'https://www.geonorge.no/geonetwork/srv/nor/resources.get?uuid=5857ec0a-8d2c-4cd8-baa2-0dc54ae213b4&access=public&fname=vern_dn_s.png'}],
      'http://www.w3.org/ns/dcat#dataQuality': [{'type': 'literal',
                                                 'value': 'Ingen prosseshistorie tilgjenglig. Målestokk varierer fra 1:5 000 til 1:20 000.'}],
      'http://purl.org/dc/terms/description': [{'type': 'literal',
                                                'value': 'Datasettet inneholder verneområder og vernede enkeltobjekt i Norge, herunder Svalbard og Jan Mayen. Datasettet gir en oversikt over hvilke områder som er vernet etter følgende lover: naturmangfoldloven av 2009, biotopvern etter viltloven av 1981, naturvernloven av 1970, lov om naturvern av 1954, lov om Jan Mayen av 1930 og lov om naturfredning av 1910. I tillegg inneholder det områder vernet etter følgende lovverk på Svalbard: Svalbardloven av 1925 og Svalbardmiljøloven av 2002. Datasettet gir også tilgang til lovforskriften som gjelder for hvert enkelt vernevedtak.',
                                                'lang': 'no'}],
      'http://www.w3.org/ns/dcat#keyword': [{'type': 'literal', 'value': 'natur', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'naturmangfoldloven av 2009', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Natur', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Norge digitalt', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'geodataloven', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'fellesDatakatalog', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Det offentlige kartgrunnlaget', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'beredskapsbase', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'naturverdier', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'naturvernområder', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'National', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Inspire', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'vern', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Protected sites', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'vernede enkeltobjekt', 'lang': 'no'}],
      'http://purl.org/dc/terms/updated': [
          {'type': 'literal', 'value': '', 'datatype': 'http://www.w3.org/2001/XMLSchema#date'}],
      'http://purl.org/dc/terms/publisher': [{'type': 'uri',
                                              'value': 'https://register.geonorge.no/organisasjoner/miljodirektoratet/dd34c8ca-5e5c-4cfd-9b25-afeadd1bcbff'}],
      'http://purl.org/dc/terms/accessRights': [
          {'type': 'uri', 'value': 'http://publications.europa.eu/resource/authority/access-right/PUBLIC'}],
      'http://www.w3.org/ns/dcat#contactPoint': [{'type': 'uri',
                                                  'value': 'https://register.geonorge.no/organisasjoner/miljodirektoratet/dd34c8ca-5e5c-4cfd-9b25-afeadd1bcbff'}],
      'http://www.w3.org/ns/dcat#granularity': [{'type': 'literal', 'value': '20000'}],
      'http://www.w3.org/ns/dcat#theme': [
          {'type': 'uri', 'value': 'http://publications.europa.eu/resource/authority/data-theme/ENVI'}, {'type': 'uri',
                                                                                                         'value': 'https://register.geonorge.no/subregister/metadata-kodelister/kartverket/nasjonal-temainndeling/kartverket/natur'}],
      'http://www.w3.org/ns/dcat#distribution': [{'type': 'uri',
                                                  'value': 'https://kartkatalog.geonorge.no/Metadata/uuid/5857ec0a-8d2c-4cd8-baa2-0dc54ae213b4/GeoJSON'},
                                                 {'type': 'uri',
                                                  'value': 'https://kartkatalog.geonorge.no/Metadata/uuid/5857ec0a-8d2c-4cd8-baa2-0dc54ae213b4/FGDB'},
                                                 {'type': 'uri',
                                                  'value': 'https://kartkatalog.geonorge.no/Metadata/uuid/5857ec0a-8d2c-4cd8-baa2-0dc54ae213b4/SOSI'}],
      'http://purl.org/dc/terms/accrualPeriodicity': [{'type': 'literal', 'value': 'asNeeded'}],
      'http://purl.org/dc/terms/license': [{'type': 'uri', 'value': 'http://data.norge.no/nlod/no/1.0'}],
      'http://purl.org/dc/terms/title': [{'type': 'literal', 'value': 'Naturvernområder', 'lang': 'no'}],
      'http://purl.org/dc/terms/identifier': [{'type': 'literal', 'value': '5857ec0a-8d2c-4cd8-baa2-0dc54ae213b4'}]}),
    ('https://kartkatalog.geonorge.no/Metadata/uuid/ce353b52-910e-404b-8a61-f7805b021bc7',
     {'http://purl.org/dc/terms/spatial': [{'type': 'bnode', 'value': '_:c6084e23f5ff29b7a1880ae3d81a0750'}],
      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
          {'type': 'uri', 'value': 'http://www.w3.org/ns/dcat#Dataset'}],
      'http://purl.org/dc/terms/description':
          [{'type': 'literal', 'value': 'Arealstatistikken viser utstrekning (oppgitt i kvadratkilometer) for fylker, '
                                        'kommuner og grunnkretser fordelt på ulike arealtyper som havflate, innsjø, skog,'
                                        ' dyrket mark, tettbebyggelse, med flere. Statistikken gjelder fra 1994 til og '
                                        'med 2018 med unntak av årene 1996, 2002, 2009, 2011, 2012.\nArealstatistikken '
                                        'etableres ut fra den administrative grensedatabasen ABAS og den landsdekkende '
                                        'kartdatabasen i målestokk 1:50 000 kalt N50 Kartdata.', 'lang': 'no'}],
      'http://www.w3.org/ns/dcat#keyword': [{'type': 'literal', 'value': 'Arealstatistikk', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Areal', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Statistikk over Norge', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Norge digitalt', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'fellesDatakatalog', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Norge', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Åpne data', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Statistikk', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Land cover', 'lang': 'no'},
                                            {'type': 'literal', 'value': 'Plan', 'lang': 'no'}],
      'http://purl.org/dc/terms/updated': [
          {'type': 'literal', 'value': '2016-04-19', 'datatype': 'http://www.w3.org/2001/XMLSchema#date'}],
      'http://purl.org/dc/terms/publisher':
          [{'type': 'uri',
            'value': 'https://register.geonorge.no/organisasjoner/kartverket/10087020-f17c-45e1-8542-02acbcf3d8a3'}],
      'http://purl.org/dc/terms/accessRights':
          [{'type': 'uri', 'value': 'http://publications.europa.eu/resource/authority/access-right/PUBLIC'}],
      'http://www.w3.org/ns/dcat#contactPoint': [
          {'type': 'uri', 'value': 'https://register.geonorge.no/organisasjoner/10087020-f17c-45e1-8542-02acbcf3d8a3'}],
      'http://www.w3.org/ns/dcat#theme': [
          {'type': 'uri', 'value': 'http://publications.europa.eu/resource/authority/data-theme/GOVE'},
          {'type': 'uri', 'value': 'http://publications.europa.eu/resource/authority/data-theme/ENVI'},
          {'type': 'uri',
           'value': 'https://register.geonorge.no/subregister/metadata-kodelister/kartverket/nasjonal-temainndeling/kartverket/plan'}],
      'http://purl.org/dc/terms/license': [
          {'type': 'uri', 'value': 'https://creativecommons.org/licenses/by/4.0/deed.no'}],
      'http://www.w3.org/ns/dcat#distribution': [
          {'type': 'uri',
           'value': 'https://kartkatalog.geonorge.no/Metadata/uuid/ce353b52-910e-404b-8a61-f7805b021bc7/Microsoft+Excel'}],
      'http://purl.org/dc/terms/identifier': [{'type': 'literal', 'value': 'ce353b52-910e-404b-8a61-f7805b021bc7'}],
      'http://purl.org/dc/terms/title': [{'type': 'literal', 'value': 'Arealstatistikk for Norge 1994 - 2019',
                                          'lang': 'no'}]}),
    ('https://dataut.vegvesen.no/dataset/60f44321-7899-4c8f-a1d9-db4846409eb7',
     {'http://purl.org/dc/terms/spatial':
          [{'type': 'uri',
            'value': 'http://sws.geonames.org/3144096/'}],
      'http://purl.org/dc/terms/language': [
          {'type': 'uri',
           'value': 'http://publications.europa.eu/resource/authority/language/NOR'}],
      'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
          {'type': 'uri',
           'value': 'http://www.w3.org/ns/dcat#Dataset'}],
      'http://purl.org/dc/terms/modified': [
          {'type': 'literal',
           'value': '2019-11-18T11:19:29.625345',
           'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime'}],
      'http://purl.org/dc/terms/description': [
          {'type': 'literal',
           'value': 'Alle registreringspliktige kjøretøy i Norge og dets eiere. Tekniske opplysninger og datoer for registrering og EU-kontroll for kjøretøy registrert i Norge.\r\n\r\nI tillegg gis enkeltoppslag på kjøretøy og eier gjennom mobilapp og SMS-tjeneste.\r\n\r\nUnderstellsregisteret inneholder opplysninger om historiske kjøretøy, og kjøretøystatistikk gir opplysninger om kjøretøybestanden i Norge.',
           'lang': 'nb'}],
      'http://www.w3.org/ns/dcat#keyword': [
          {'type': 'literal',
           'value': 'kjøretøy'}],
      'http://purl.org/dc/terms/issued': [
          {'type': 'literal',
           'value': '2017-03-10T08:55:16.146898',
           'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime'}],
      'http://purl.org/dc/terms/accessRights': [
          {'type': 'uri',
           'value': 'http://publications.europa.eu/resource/authority/access-right/PUBLIC'}],
      'http://purl.org/dc/terms/publisher': [
          {'type': 'uri',
           'value': 'https://dataut.vegvesen.no/organization/e6d3dc7a-752e-418b-9afd-36533b370285'}],
      'http://www.w3.org/ns/dcat#theme': [
          {'type': 'uri',
           'value': 'https://publications.europa.eu/resource/authority/data-theme/TRAN'}],
      'http://www.w3.org/ns/dcat#distribution': [
          {'type': 'uri',
           'value': 'https://dataut.vegvesen.no/dataset/60f44321-7899-4c8f-a1d9-db4846409eb7/resource/0cbd94c5-d2f1-462a-81de-de2947b50fcf'},
          {'type': 'uri',
           'value': 'https://dataut.vegvesen.no/dataset/60f44321-7899-4c8f-a1d9-db4846409eb7/resource/9318648a-1afb-4865-b99c-70f78e5d69f3'},
          {'type': 'uri',
           'value': 'https://dataut.vegvesen.no/dataset/60f44321-7899-4c8f-a1d9-db4846409eb7/resource/301d1bf6-f146-4cdb-be63-d5eda947324c'}],
      'http://purl.org/dc/terms/title': [
          {'type': 'literal',
           'value': 'Kjøretøyopplysninger',
           'lang': 'nb'}],
      'http://purl.org/dc/terms/identifier': [
          {'type': 'literal',
           'value': 'http://vegvesen.no/datasett/id_ikke_permanent/kjoretoyopplysninger'}]})
]
mock_distributions = [
    ('_:36016e0cbd5e5a436c2317821f2b8c9f', {'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
        {'type': 'uri', 'value': 'http://www.w3.org/ns/dcat#Distribution'}], 'http://purl.org/dc/terms/format': [
        {'type': 'literal', 'value': 'XLSX'}],
        'http://www.w3.org/ns/dcat#accessURL': [
            {'type': 'uri',
             'value': 'https://www.oslo.kommune.no/politikk-og-administrasjon/politikk/budsjett-regnskap-og-'
                      'rapportering/tidligere-ars-budsjetter-og-regnskap/budsjett-og-regnskap-for-2014/'}],
        'http://purl.org/dc/terms/description': [
            {'type': 'literal',
             'value': 'Oslo kommune - byrådets budsjettforslag 2014 og økonomiplan 2014-2017',
             'lang': 'nb'}
        ],
        'http://purl.org/dc/terms/license': [{'type': 'bnode',
                                              'value': '_:7848e2c978fce16057d67bb9e326b13a'}]}),
    ('https://kartkatalog.geonorge.no/Metadata/uuid/de19fbbf-3734-47a0-89f5-6c5769071cdd/FGDB', {
        'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
            {'type': 'uri', 'value': 'http://www.w3.org/ns/dcat#Distribution'}],
        'http://purl.org/dc/terms/format': [
            {'type': 'literal', 'value': 'FGDB'}
        ],
        'http://www.w3.org/ns/dcat#accessURL': [
            {'type': 'uri',
             'value': 'https://kartkatalog.geonorge.no/metadata/uuid/de19fbbf-3734-47a0-89f5-6c5769071cdd'}
        ],
        'http://www.w3.org/ns/adms#status': [
            {'type': 'uri', 'value': 'http://purl.org/adms/status/onGoing'}
        ],
        'http://purl.org/dc/terms/description': [
            {'type': 'literal',
             'value': 'Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet'}
        ],
        'http://purl.org/dc/terms/license': [
            {'type': 'uri', 'value': 'http://creativecommons.org/licenses/by/3.0/no/'}
        ],
        'http://purl.org/dc/terms/title': [
            {'type': 'literal', 'value': 'Geonorge nedlastning', 'lang': 'no'}]}),
    ('https://kartkatalog.geonorge.no/Metadata/uuid/b2d5aaf8-79ac-40f3-9cd6-fdc30bc42ea1/FGDB',
     {
         'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
             {
                 'type': 'uri',
                 'value': 'http://www.w3.org/ns/dcat#Distribution'
             }
         ],
         'http://purl.org/dc/terms/format': [{'type': 'literal', 'value': 'FGDB'}],
         'http://www.w3.org/ns/dcat#accessURL': [
             {'type': 'uri',
              'value': 'https://kartkatalog.geonorge.no/metadata/uuid/b2d5aaf8-79ac-40f3-9cd6-fdc30bc42ea1'}
         ],
         'http://www.w3.org/ns/adms#status': [
             {'type': 'uri', 'value': 'http://purl.org/adms/status/onGoing'}
         ],
         'http://purl.org/dc/terms/description': [{'type': 'literal',
                                                   'value': 'Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet'}],
         'http://purl.org/dc/terms/license': [
             {'type': 'uri', 'value': 'http://data.norge.no/nlod/no/1.0'}
         ],
         'http://purl.org/dc/terms/title': [
             {'type': 'literal', 'value': 'Geonorge nedlastning', 'lang': 'no'}
         ]
     }
     ),
    (
        '_:faf29c364e4520c1db6af9ce27818a1b', {'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
            {'type': 'uri', 'value': 'http://www.w3.org/ns/dcat#Distribution'}],
            'http://purl.org/dc/terms/format': [
                {'type': 'literal', 'value': 'JSON'},
                {'type': 'literal', 'value': 'CSV'},
                {'type': 'literal', 'value': 'RDF'}],
            'http://www.w3.org/ns/dcat#accessURL': [
                {'type': 'uri', 'value': 'http://kulturnav.org/'}],
            'http://purl.org/dc/terms/description': [{'type': 'literal',
                                                      'value': 'Data fra KulturNAV tilgjengelig i JSON, CSV og RDF/XML',
                                                      'lang': 'nb'}],
            'http://purl.org/dc/terms/license': [{'type': 'bnode',
                                                  'value': '_:86687ee4606f4f64689d40920541fe38'}]})]
mock_licence_documents = [
    ('_:2fb1be20b4b19062bd2425899b157551',
     {'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
         {'type': 'uri', 'value': 'http://difi.no/skosno#Definisjon'}
     ],
         'http://www.w3.org/2000/01/rdf-schema#label': [
             {'type': 'literal', 'value': 'barn som ikke har fylt 18 år innen utløpet av skatteleggingsperioden',
              'lang': 'nb'}]}),
    ('https://kartkatalog.geonorge.no/Metadata/uuid/554d9e3f-18d1-40f2-bf23-5d104a8cb1ff',
     {
         'http://purl.org/dc/terms/spatial': [{'type': 'bnode', 'value': '_:f9c14e33ab8f2bd4d6594e8215f0463f'}],
         'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
             {'type': 'uri', 'value': 'http://www.w3.org/ns/dcat#Dataset'}],
         'http://purl.org/dc/terms/description': [
             {
                 'type': 'literal',
                 'value': 'The dataset shows national, county and municipal divisions within the country. The '
                          'municipalities are delimited by National Border, Outer Limit of Territorial Waters 12 '
                          'Nautical Miles, Agreed Delimitation Line, county boundary and municipal boundary. The '
                          'units include properties which indicate official municipal numbers.',
                 'lang': 'no'}],
         'http://www.w3.org/ns/dcat#dataQuality': [
             {'type': 'literal', 'value': 'Ingen prosesshistorie tilgjengelig'}
         ],
         'http://xmlns.com/foaf/0.1/thumbnail': [
             {
                 'type': 'uri',
                 'value': 'https://editor.geonorge.no/thumbnails/554d9e3f-18d1-40f2-bf23-5d104a8cb1ff_20180227133418_adm.PNG'}
         ],
         'http://www.w3.org/ns/dcat#keyword': [
             {'type': 'literal', 'value': 'ELF', 'lang': 'no'},
             {'type': 'literal', 'value': 'INSPIRE', 'lang': 'no'},
             {'type': 'literal', 'value': 'National', 'lang': 'no'},
             {'type': 'literal', 'value': 'geodataloven', 'lang': 'no'},
             {'type': 'literal', 'value': 'Norge digitalt', 'lang': 'no'},
             {'type': 'literal', 'value': 'Basis geodata', 'lang': 'no'},
             {'type': 'literal', 'value': 'fellesDatakatalog', 'lang': 'no'},
             {'type': 'literal', 'value': 'Administrative units', 'lang': 'no'},
             {'type': 'literal', 'value': 'Inspire', 'lang': 'no'}
         ],
         'http://purl.org/dc/terms/updated': [
             {'type': 'literal', 'value': '', 'datatype': 'http://www.w3.org/2001/XMLSchema#date'}],
         'http://purl.org/dc/terms/publisher':
             [
                 {'type': 'uri',
                  'value': 'https://register.geonorge.no/organisasjoner/kartverket/10087020-f17c-45e1-8542-02acbcf3d8a3'}
             ],
         'http://purl.org/dc/terms/accessRights': [
             {'type': 'uri', 'value': 'http://publications.europa.eu/resource/authority/access-right/PUBLIC'}],
         'http://www.w3.org/ns/dcat#contactPoint': [{'type': 'uri',
                                                     'value': 'https://register.geonorge.no/organisasjoner/10087020-f17c-45e1-8542-02acbcf3d8a3'}],
         'http://www.w3.org/ns/dcat#granularity': [{'type': 'literal', 'value': '100000'}],
         'http://www.w3.org/ns/dcat#theme': [
             {'type': 'uri', 'value': 'http://publications.europa.eu/resource/authority/data-theme/GOVE'},
             {'type': 'uri', 'value': 'http://publications.europa.eu/resource/authority/data-theme/REGI'},
             {'type': 'uri',
              'value': 'https://register.geonorge.no/subregister/metadata-kodelister/kartverket/nasjonal-temainndeling/kartverket/basis-geodata'}],
         'http://purl.org/dc/terms/accrualPeriodicity': [{'type': 'literal', 'value': 'unknown'}],
         'http://www.w3.org/ns/dcat#distribution': [{'type': 'uri',
                                                     'value': 'https://kartkatalog.geonorge.no/Metadata/uuid/554d9e3f-18d1-40f2-bf23-5d104a8cb1ff/GML'}],
         'http://purl.org/dc/terms/license': [
             {'type': 'uri', 'value': 'https://creativecommons.org/licenses/by/4.0/'}],
         'http://purl.org/dc/terms/identifier': [
             {'type': 'literal', 'value': '554d9e3f-18d1-40f2-bf23-5d104a8cb1ff'}],
         'http://purl.org/dc/terms/title': [
             {'type': 'literal', 'value': 'INSPIRE Administrative units', 'lang': 'no'}]}),
    ('_:dd7d83d7d3a20af0487d59871f9eb3d5',
     {'http://www.w3.org/1999/02/22-rdf-syntax-ns#value': [{'type': 'literal', 'value': 'asdasd', 'lang': 'nb'}]}),
    ('_:4dc09661999ff3199e84832fc69e4e3a',
     {'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': [
         {'type': 'uri', 'value': 'http://purl.org/dc/terms/Standard'},
         {'type': 'uri', 'value': 'http://www.w3.org/2004/02/skos/core#Concept'}
     ],
         'http://purl.org/dc/terms/source': [
             {'type': 'literal', 'value': 'http://hotell.difi.no/application.wadl'}]})
]
mock_catalogs = [
    ("http://registration-api:8080/catalogs/911259583", {
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/911259583"
            }
        ],
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Catalog"
            }
        ],
        "http://purl.org/dc/terms/title": [
            {
                "type": "literal",
                "value": "Datakatalog for VÅLER I ØSTFOLD OG VIKHAMMER",
                "lang": "nb"
            }
        ],
        "http://www.w3.org/ns/dcat#dataset": [
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/85875858585858a"
            }
        ]
    }),
    ("http://registration-api:8080/catalogs/876543231", {
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/911259583"
            }
        ],
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Catalog"
            }
        ],
        "http://purl.org/dc/terms/title": [
            {
                "type": "literal",
                "value": "Datakatalog without dcat dataset",
                "lang": "nb"
            }
        ]
    }),
    ("http://registration-api:8080/catalogs/12346890", {
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/911259583"
            }
        ],
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Catalog"
            }
        ],
        "http://purl.org/dc/terms/title": [
            {
                "type": "literal",
                "value": "Datakatalog with dcat dataset",
                "lang": "nb"
            }
        ],
        "http://www.w3.org/ns/dcat#dataset": [
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/ebd0aa41-da69-4f37-a44a-2d10f127a68a"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/3749f2c6-0d16-4bfb-b74f-6597b3705e2e"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/c6b9e443-12a4-4d29-854a-0f6eda682858"
            },
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/910244132/datasets/a4c9556f-9874-400b-80ad-7cd74cfb3c23"
            }]
    }),
    ("http://registration-api:8080/catalogs/911527170", {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Catalog"
            }
        ],
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/911527170"
            }
        ],
        "http://www.w3.org/ns/dcat#dataset": [
            {
                "type": "uri",
                "value": "http://brreg.no/catalogs/911527170/datasets/ef06c5b3-c440-4948-9189-c03de9b4c52b"
            }
        ],
        "http://purl.org/dc/terms/title": [
            {
                "type": "literal",
                "value": "Datakatalog for SKATVAL OG BREIVIKBOTN",
                "lang": "nb"
            }
        ]
    })
]
mock_open_licenses = [
    OpenLicense("http://creativecommons.org/licenses/by/4.0/"),
    OpenLicense("http://creativecommons.org/licenses/by/4.0/deed.no"),
    OpenLicense("http://creativecommons.org/publicdomain/zero/1.0/"),
    OpenLicense("http://data.norge.no/nlod/"),
    OpenLicense("http://data.norge.no/nlod/no/"),
    OpenLicense("http://data.norge.no/nlod/no/1.0"),
    OpenLicense("http://data.norge.no/nlod/no/2.0")
]
mock_distribution_b_node_in_dataset = {
    "http://www.w3.org/ns/dcat#distribution": [{
        "type": "uri",
        "value": "https://dataut.vegvesen.no/dataset/66adf913-c48e-40e7-a7fb-586e542c42ff/resource/0a51c171-5330-4e13"
                 "-8bdc-e15fefd7c822 "
    }],
    "http://purl.org/dc/terms/identifier": [{
        "type": "literal",
        "value": "http://vegvesen.no/datasett/id_ikke_permanent/elveg-vbase"
    }
    ],
    "http://purl.org/dc/terms/title": [{
        "type": "literal",
        "value": "Kart over vegnett \u2013 Elveg",
        "lang": "nb"
    }
        , {
            "type": "literal",
            "value": "Map over road networks - Elveg",
            "lang": "en"
        }
    ]
}
