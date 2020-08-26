import json

import pytest

from src.elasticsearch.datasets import insert_datasets, merge_dataset_information
from src.elasticsearch.queries import AggregationQuery
from src.elasticsearch.utils import EsMappings
from src.rdf_namespaces import JSON_LD
from src.utils import ServiceKey


@pytest.mark.unit
def test_dry_run():
    #    insert_datasets()
    result = AggregationQuery(ServiceKey.DATA_SETS).build()
    x = json.dumps(result)
    x = 0


@pytest.mark.unit
def test_merge_dataset_information_with_node_refs():
    dataset_with_orgpath = {
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/910244132"
            }
        ],
        "http://purl.org/dc/terms/accessRights": [
            {
                "type": "uri",
                "value": "http://publications.europa.eu/resource/authority/access-right/RESTRICTED"
            }
        ],
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Dataset"
            }
        ],
        "http://purl.org/dc/terms/modified": [
            {
                "type": "literal",
                "value": "2019-01-09",
                "datatype": "http://www.w3.org/2001/XMLSchema#date"
            }
        ],
        "http://purl.org/dc/terms/description": [
            {
                "type": "literal",
                "value": "Bare tull",
                "lang": "nb"
            }
        ],
        "http://www.w3.org/ns/dcat#theme": [
            {
                "type": "uri",
                "value": "http://publications.europa.eu/resource/authority/data-theme/GOVE"
            }
        ],
        "http://www.w3.org/ns/dcat#distribution": [
            {
                "type": "uri",
                "value": "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/SOSI"
            },
            {
                "type": "uri",
                "value": "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/GML"
            }
        ],
        EsMappings.ORG_PATH: "/ANNET/MOCK PATH",
        EsMappings.NODE_URI: "http://brreg.no/catalogs/910244132/datasets/987654-12hhhj-123"
    }
    distributions = [
        {"https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/SOSI": {
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#Distribution"
                }
            ],
            "http://purl.org/dc/terms/format": [
                {
                    "type": "literal",
                    "value": "SOSI"
                }
            ],
            "http://www.w3.org/ns/dcat#accessURL": [
                {
                    "type": "uri",
                    "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                }
            ],
            "http://www.w3.org/ns/adms#status": [
                {
                    "type": "uri",
                    "value": "http://purl.org/adms/status/historicalArchive"
                }
            ],
            "http://purl.org/dc/terms/description": [
                {
                    "type": "literal",
                    "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                }
            ],
            "http://purl.org/dc/terms/license": [
                {
                    "type": "uri",
                    "value": "http://data.norge.no/nlod/no/1.0"
                }
            ],
            "http://purl.org/dc/terms/title": [
                {
                    "type": "literal",
                    "value": "Geonorge nedlastning",
                    "lang": "no"
                }
            ]
        }},
        {
            "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/HTML": {
                "http://www.w3.org/ns/dcat#accessURL": [
                    {
                        "type": "uri",
                        "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                    }
                ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                    {
                        "type": "uri",
                        "value": "http://www.w3.org/ns/dcat#Distribution"
                    }
                ],
                "http://purl.org/dc/terms/format": [
                    {
                        "type": "literal",
                        "value": "GML"
                    }
                ],
                "http://www.w3.org/ns/adms#status": [
                    {
                        "type": "uri",
                        "value": "http://purl.org/adms/status/historicalArchive"
                    }
                ],
                "http://purl.org/dc/terms/description": [
                    {
                        "type": "literal",
                        "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                    }
                ],
                "http://purl.org/dc/terms/license": [
                    {
                        "type": "uri",
                        "value": "http://data.norge.no/nlod/no/1.0"
                    }
                ],
                "http://purl.org/dc/terms/title": [
                    {
                        "type": "literal",
                        "value": "Geonorge nedlastning",
                        "lang": "no"
                    }
                ]
            }
        },
        {
            "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/GML": {
                "http://www.w3.org/ns/dcat#accessURL": [
                    {
                        "type": "uri",
                        "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                    }
                ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                    {
                        "type": "uri",
                        "value": "http://www.w3.org/ns/dcat#Distribution"
                    }
                ],
                "http://purl.org/dc/terms/format": [
                    {
                        "type": "literal",
                        "value": "GML"
                    }
                ],
                "http://www.w3.org/ns/adms#status": [
                    {
                        "type": "uri",
                        "value": "http://purl.org/adms/status/historicalArchive"
                    }
                ],
                "http://purl.org/dc/terms/description": [
                    {
                        "type": "literal",
                        "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                    }
                ],
                "http://purl.org/dc/terms/license": [
                    {
                        "type": "uri",
                        "value": "http://data.norge.no/nlod/no/1.0"
                    }
                ],
                "http://purl.org/dc/terms/title": [
                    {
                        "type": "literal",
                        "value": "Geonorge nedlastning",
                        "lang": "no"
                    }
                ]
            }
        },
        {
            "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/XML": {
                "http://www.w3.org/ns/dcat#accessURL": [
                    {
                        "type": "uri",
                        "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                    }
                ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                    {
                        "type": "uri",
                        "value": "http://www.w3.org/ns/dcat#Distribution"
                    }
                ],
                "http://purl.org/dc/terms/format": [
                    {
                        "type": "literal",
                        "value": "GML"
                    }
                ],
                "http://www.w3.org/ns/adms#status": [
                    {
                        "type": "uri",
                        "value": "http://purl.org/adms/status/historicalArchive"
                    }
                ],
                "http://purl.org/dc/terms/description": [
                    {
                        "type": "literal",
                        "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                    }
                ],
                "http://purl.org/dc/terms/license": [
                    {
                        "type": "uri",
                        "value": "http://data.norge.no/nlod/no/1.0"
                    }
                ],
                "http://purl.org/dc/terms/title": [
                    {
                        "type": "literal",
                        "value": "Geonorge nedlastning",
                        "lang": "no"
                    }
                ]
            }
        }

    ]
    meta_data_list = [
        {"https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b7611952-9341-37a8-afcf-a1c5499805a5": {
            "http://xmlns.com/foaf/0.1/primaryTopic": [
                {
                    "type": "uri",
                    "value": "http://brreg.no/catalogs/910244132/datasets/17ed5a7d-1a22-49f4-a1d6-25f7d90dfa6d"
                }
            ],
            "http://purl.org/dc/terms/isPartOf": [
                {
                    "type": "uri",
                    "value": "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/821c273e-c4b0-3807-8d54-f54998747507"
                }
            ],
            "http://purl.org/dc/terms/identifier": [
                {
                    "type": "literal",
                    "value": "b7611952-9341-37a8-afcf-a1c5499805a5"
                }
            ],
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#CatalogRecord"
                }
            ]}},
        {"https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b12345-9876-ghg": {
            "http://xmlns.com/foaf/0.1/primaryTopic": [
                {
                    "type": "uri",
                    "value": "http://brreg.no/catalogs/910244132/datasets/987654-12hhhj-123"
                }
            ],
            "http://purl.org/dc/terms/isPartOf": [
                {
                    "type": "uri",
                    "value": "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/821c273e-c4b0-3807-8d54-f54998747507"
                }
            ],
            "http://purl.org/dc/terms/identifier": [
                {
                    "type": "literal",
                    "value": "b7611952-9341-37a8-afcf-a1c5499805a5"
                }
            ],
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#CatalogRecord"
                }
            ]}},
        {"https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b1285678-jhj7p": {
            "http://xmlns.com/foaf/0.1/primaryTopic": [
                {
                    "type": "uri",
                    "value": "http://brreg.no/catalogs/910244132/datasets/987654-12hhhj-123-hkjh34-ah7"
                }
            ],
            "http://purl.org/dc/terms/isPartOf": [
                {
                    "type": "uri",
                    "value": "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/821c273e-c4b0-3807-8d54-f54998747507"
                }
            ],
            "http://purl.org/dc/terms/identifier": [
                {
                    "type": "literal",
                    "value": "b7611952-9341-37a8-afcf-a1c5499805a5"
                }
            ],
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#CatalogRecord"
                }
            ]}}
    ]
    result = merge_dataset_information(dataset=dataset_with_orgpath,
                                       distributions=distributions,
                                       records=meta_data_list)
    result_keys = result.keys()
    assert EsMappings.RECORD in result_keys
    assert len(result[EsMappings.RECORD]) == 1
    assert \
        result[EsMappings.RECORD][0]["https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b12345-9876-ghg"][
            "http://xmlns.com/foaf/0.1/primaryTopic"][0]["value"] == meta_data_list[1][
            "https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b12345-9876-ghg"][
            "http://xmlns.com/foaf/0.1/primaryTopic"][0]["value"]
    assert \
        result[EsMappings.RECORD][0]["https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b12345-9876-ghg"][
            "http://xmlns.com/foaf/0.1/primaryTopic"][0]["value"] == result[EsMappings.NODE_URI]
    assert len(dataset_with_orgpath["http://www.w3.org/ns/dcat#distribution"]) == 2
    expected_dist_formats = ["SOSI", "GML"]
    assert result["http://www.w3.org/ns/dcat#distribution"][0][JSON_LD.DCT.format][0]["value"] in expected_dist_formats
    assert result["http://www.w3.org/ns/dcat#distribution"][1][JSON_LD.DCT.format][0]["value"] in expected_dist_formats


@pytest.mark.unit
def test_merge_dataset_information_with_inline_distributions():
    dataset_with_orgpath = {
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/910244132"
            }
        ],
        "http://purl.org/dc/terms/accessRights": [
            {
                "type": "uri",
                "value": "http://publications.europa.eu/resource/authority/access-right/RESTRICTED"
            }
        ],
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Dataset"
            }
        ],
        "http://purl.org/dc/terms/modified": [
            {
                "type": "literal",
                "value": "2019-01-09",
                "datatype": "http://www.w3.org/2001/XMLSchema#date"
            }
        ],
        "http://purl.org/dc/terms/description": [
            {
                "type": "literal",
                "value": "Bare tull",
                "lang": "nb"
            }
        ],
        "http://www.w3.org/ns/dcat#theme": [
            {
                "type": "uri",
                "value": "http://publications.europa.eu/resource/authority/data-theme/GOVE"
            }
        ],
        "http://www.w3.org/ns/dcat#distribution": [
            {"http://www.w3.org/ns/dcat#accessURL": [
                {
                    "type": "uri",
                    "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                }
            ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                    {
                        "type": "uri",
                        "value": "http://www.w3.org/ns/dcat#Distribution"
                    }
                ],
                "http://purl.org/dc/terms/format": [
                    {
                        "type": "literal",
                        "value": "HTML"
                    }
                ],
                "http://www.w3.org/ns/adms#status": [
                    {
                        "type": "uri",
                        "value": "http://purl.org/adms/status/historicalArchive"
                    }
                ],
                "http://purl.org/dc/terms/description": [
                    {
                        "type": "literal",
                        "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                    }
                ],
                "http://purl.org/dc/terms/license": [
                    {
                        "type": "uri",
                        "value": "http://data.norge.no/nlod/no/1.0"
                    }
                ],
                "http://purl.org/dc/terms/title": [
                    {
                        "type": "literal",
                        "value": "Geonorge nedlastning",
                        "lang": "no"
                    }
                ]}
        ],
        EsMappings.ORG_PATH: "/ANNET/MOCK PATH",
        EsMappings.NODE_URI: "http://brreg.no/catalogs/910244132/datasets/987654-12hhhj-123"
    }
    distributions = [
        {"https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/SOSI": {
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#Distribution"
                }
            ],
            "http://purl.org/dc/terms/format": [
                {
                    "type": "literal",
                    "value": "SOSI"
                }
            ],
            "http://www.w3.org/ns/dcat#accessURL": [
                {
                    "type": "uri",
                    "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                }
            ],
            "http://www.w3.org/ns/adms#status": [
                {
                    "type": "uri",
                    "value": "http://purl.org/adms/status/historicalArchive"
                }
            ],
            "http://purl.org/dc/terms/description": [
                {
                    "type": "literal",
                    "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                }
            ],
            "http://purl.org/dc/terms/license": [
                {
                    "type": "uri",
                    "value": "http://data.norge.no/nlod/no/1.0"
                }
            ],
            "http://purl.org/dc/terms/title": [
                {
                    "type": "literal",
                    "value": "Geonorge nedlastning",
                    "lang": "no"
                }
            ]
        }},
        {
            "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/HTML": {
                "http://www.w3.org/ns/dcat#accessURL": [
                    {
                        "type": "uri",
                        "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                    }
                ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                    {
                        "type": "uri",
                        "value": "http://www.w3.org/ns/dcat#Distribution"
                    }
                ],
                "http://purl.org/dc/terms/format": [
                    {
                        "type": "literal",
                        "value": "HTML"
                    }
                ],
                "http://www.w3.org/ns/adms#status": [
                    {
                        "type": "uri",
                        "value": "http://purl.org/adms/status/historicalArchive"
                    }
                ],
                "http://purl.org/dc/terms/description": [
                    {
                        "type": "literal",
                        "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                    }
                ],
                "http://purl.org/dc/terms/license": [
                    {
                        "type": "uri",
                        "value": "http://data.norge.no/nlod/no/1.0"
                    }
                ],
                "http://purl.org/dc/terms/title": [
                    {
                        "type": "literal",
                        "value": "Geonorge nedlastning",
                        "lang": "no"
                    }
                ]
            }
        },
        {
            "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/GML": {
                "http://www.w3.org/ns/dcat#accessURL": [
                    {
                        "type": "uri",
                        "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                    }
                ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                    {
                        "type": "uri",
                        "value": "http://www.w3.org/ns/dcat#Distribution"
                    }
                ],
                "http://purl.org/dc/terms/format": [
                    {
                        "type": "literal",
                        "value": "GML"
                    }
                ],
                "http://www.w3.org/ns/adms#status": [
                    {
                        "type": "uri",
                        "value": "http://purl.org/adms/status/historicalArchive"
                    }
                ],
                "http://purl.org/dc/terms/description": [
                    {
                        "type": "literal",
                        "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                    }
                ],
                "http://purl.org/dc/terms/license": [
                    {
                        "type": "uri",
                        "value": "http://data.norge.no/nlod/no/1.0"
                    }
                ],
                "http://purl.org/dc/terms/title": [
                    {
                        "type": "literal",
                        "value": "Geonorge nedlastning",
                        "lang": "no"
                    }
                ]
            }
        },
        {
            "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/XML": {
                "http://www.w3.org/ns/dcat#accessURL": [
                    {
                        "type": "uri",
                        "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                    }
                ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                    {
                        "type": "uri",
                        "value": "http://www.w3.org/ns/dcat#Distribution"
                    }
                ],
                "http://purl.org/dc/terms/format": [
                    {
                        "type": "literal",
                        "value": "GML"
                    }
                ],
                "http://www.w3.org/ns/adms#status": [
                    {
                        "type": "uri",
                        "value": "http://purl.org/adms/status/historicalArchive"
                    }
                ],
                "http://purl.org/dc/terms/description": [
                    {
                        "type": "literal",
                        "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                    }
                ],
                "http://purl.org/dc/terms/license": [
                    {
                        "type": "uri",
                        "value": "http://data.norge.no/nlod/no/1.0"
                    }
                ],
                "http://purl.org/dc/terms/title": [
                    {
                        "type": "literal",
                        "value": "Geonorge nedlastning",
                        "lang": "no"
                    }
                ]
            }
        }
    ]
    meta_data_list = [
        {"https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b7611952-9341-37a8-afcf-a1c5499805a5": {
            "http://xmlns.com/foaf/0.1/primaryTopic": [
                {
                    "type": "uri",
                    "value": "http://brreg.no/catalogs/910244132/datasets/17ed5a7d-1a22-49f4-a1d6-25f7d90dfa6d"
                }
            ],
            "http://purl.org/dc/terms/isPartOf": [
                {
                    "type": "uri",
                    "value": "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/821c273e-c4b0-3807-8d54-f54998747507"
                }
            ],
            "http://purl.org/dc/terms/identifier": [
                {
                    "type": "literal",
                    "value": "b7611952-9341-37a8-afcf-a1c5499805a5"
                }
            ],
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#CatalogRecord"
                }
            ]}},
        {"https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b12345-9876-ghg": {
            "http://xmlns.com/foaf/0.1/primaryTopic": [
                {
                    "type": "uri",
                    "value": "http://brreg.no/catalogs/910244132/datasets/987654-12hhhj-123"
                }
            ],
            "http://purl.org/dc/terms/isPartOf": [
                {
                    "type": "uri",
                    "value": "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/821c273e-c4b0-3807-8d54-f54998747507"
                }
            ],
            "http://purl.org/dc/terms/identifier": [
                {
                    "type": "literal",
                    "value": "b7611952-9341-37a8-afcf-a1c5499805a5"
                }
            ],
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#CatalogRecord"
                }
            ]}},
        {"https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b1285678-jhj7p": {
            "http://xmlns.com/foaf/0.1/primaryTopic": [
                {
                    "type": "uri",
                    "value": "http://brreg.no/catalogs/910244132/datasets/987654-12hhhj-123-hkjh34-ah7"
                }
            ],
            "http://purl.org/dc/terms/isPartOf": [
                {
                    "type": "uri",
                    "value": "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/821c273e-c4b0-3807-8d54-f54998747507"
                }
            ],
            "http://purl.org/dc/terms/identifier": [
                {
                    "type": "literal",
                    "value": "b7611952-9341-37a8-afcf-a1c5499805a5"
                }
            ],
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#CatalogRecord"
                }
            ]}}
    ]
    result = merge_dataset_information(dataset=dataset_with_orgpath,
                                       distributions=distributions,
                                       records=meta_data_list)
    assert len(dataset_with_orgpath["http://www.w3.org/ns/dcat#distribution"]) == 1
    assert result["http://www.w3.org/ns/dcat#distribution"][0][JSON_LD.DCT.format][0]["value"] == "HTML"


@pytest.mark.unit
def test_merge_dataset_information_with_mixed_distributions():
    dataset_with_orgpath = {
        "http://purl.org/dc/terms/publisher": [
            {
                "type": "uri",
                "value": "https://data.brreg.no/enhetsregisteret/api/enheter/910244132"
            }
        ],
        "http://purl.org/dc/terms/accessRights": [
            {
                "type": "uri",
                "value": "http://publications.europa.eu/resource/authority/access-right/RESTRICTED"
            }
        ],
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
            {
                "type": "uri",
                "value": "http://www.w3.org/ns/dcat#Dataset"
            }
        ],
        "http://purl.org/dc/terms/modified": [
            {
                "type": "literal",
                "value": "2019-01-09",
                "datatype": "http://www.w3.org/2001/XMLSchema#date"
            }
        ],
        "http://purl.org/dc/terms/description": [
            {
                "type": "literal",
                "value": "Bare tull",
                "lang": "nb"
            }
        ],
        "http://www.w3.org/ns/dcat#theme": [
            {
                "type": "uri",
                "value": "http://publications.europa.eu/resource/authority/data-theme/GOVE"
            }
        ],
        "http://www.w3.org/ns/dcat#distribution": [
            {
                "http://www.w3.org/ns/dcat#accessURL": [
                    {
                        "type": "uri",
                        "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                    }
                ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                    {
                        "type": "uri",
                        "value": "http://www.w3.org/ns/dcat#Distribution"
                    }
                ],
                "http://purl.org/dc/terms/format": [
                    {
                        "type": "literal",
                        "value": "HTML"
                    }
                ],
                "http://www.w3.org/ns/adms#status": [
                    {
                        "type": "uri",
                        "value": "http://purl.org/adms/status/historicalArchive"
                    }
                ],
                "http://purl.org/dc/terms/description": [
                    {
                        "type": "literal",
                        "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                    }
                ],
                "http://purl.org/dc/terms/license": [
                    {
                        "type": "uri",
                        "value": "http://data.norge.no/nlod/no/1.0"
                    }
                ],
                "http://purl.org/dc/terms/title": [
                    {
                        "type": "literal",
                        "value": "Geonorge nedlastning",
                        "lang": "no"
                    }
                ]
            },
            {
                "type": "uri",
                "value": "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/SOSI"
            },
            {
                "type": "uri",
                "value": "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/GML"
            }

        ],
        EsMappings.ORG_PATH: "/ANNET/MOCK PATH",
        EsMappings.NODE_URI: "http://brreg.no/catalogs/910244132/datasets/987654-12hhhj-123"
    }
    distributions = [
        {"https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/SOSI": {
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#Distribution"
                }
            ],
            "http://purl.org/dc/terms/format": [
                {
                    "type": "literal",
                    "value": "SOSI"
                }
            ],
            "http://www.w3.org/ns/dcat#accessURL": [
                {
                    "type": "uri",
                    "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                }
            ],
            "http://www.w3.org/ns/adms#status": [
                {
                    "type": "uri",
                    "value": "http://purl.org/adms/status/historicalArchive"
                }
            ],
            "http://purl.org/dc/terms/description": [
                {
                    "type": "literal",
                    "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                }
            ],
            "http://purl.org/dc/terms/license": [
                {
                    "type": "uri",
                    "value": "http://data.norge.no/nlod/no/1.0"
                }
            ],
            "http://purl.org/dc/terms/title": [
                {
                    "type": "literal",
                    "value": "Geonorge nedlastning",
                    "lang": "no"
                }
            ]
        }},
        {
            "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/HTML": {
                "http://www.w3.org/ns/dcat#accessURL": [
                    {
                        "type": "uri",
                        "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                    }
                ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                    {
                        "type": "uri",
                        "value": "http://www.w3.org/ns/dcat#Distribution"
                    }
                ],
                "http://purl.org/dc/terms/format": [
                    {
                        "type": "literal",
                        "value": "HTML"
                    }
                ],
                "http://www.w3.org/ns/adms#status": [
                    {
                        "type": "uri",
                        "value": "http://purl.org/adms/status/historicalArchive"
                    }
                ],
                "http://purl.org/dc/terms/description": [
                    {
                        "type": "literal",
                        "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                    }
                ],
                "http://purl.org/dc/terms/license": [
                    {
                        "type": "uri",
                        "value": "http://data.norge.no/nlod/no/1.0"
                    }
                ],
                "http://purl.org/dc/terms/title": [
                    {
                        "type": "literal",
                        "value": "Geonorge nedlastning",
                        "lang": "no"
                    }
                ]
            }
        },
        {
            "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/GML": {
                "http://www.w3.org/ns/dcat#accessURL": [
                    {
                        "type": "uri",
                        "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                    }
                ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                    {
                        "type": "uri",
                        "value": "http://www.w3.org/ns/dcat#Distribution"
                    }
                ],
                "http://purl.org/dc/terms/format": [
                    {
                        "type": "literal",
                        "value": "GML"
                    }
                ],
                "http://www.w3.org/ns/adms#status": [
                    {
                        "type": "uri",
                        "value": "http://purl.org/adms/status/historicalArchive"
                    }
                ],
                "http://purl.org/dc/terms/description": [
                    {
                        "type": "literal",
                        "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                    }
                ],
                "http://purl.org/dc/terms/license": [
                    {
                        "type": "uri",
                        "value": "http://data.norge.no/nlod/no/1.0"
                    }
                ],
                "http://purl.org/dc/terms/title": [
                    {
                        "type": "literal",
                        "value": "Geonorge nedlastning",
                        "lang": "no"
                    }
                ]
            }
        },
        {
            "https://kartkatalog.geonorge.no/Metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811/XML": {
                "http://www.w3.org/ns/dcat#accessURL": [
                    {
                        "type": "uri",
                        "value": "https://kartkatalog.geonorge.no/metadata/uuid/d02dc4bd-77d5-4b3b-a316-5a488b6fe811"
                    }
                ],
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                    {
                        "type": "uri",
                        "value": "http://www.w3.org/ns/dcat#Distribution"
                    }
                ],
                "http://purl.org/dc/terms/format": [
                    {
                        "type": "literal",
                        "value": "GML"
                    }
                ],
                "http://www.w3.org/ns/adms#status": [
                    {
                        "type": "uri",
                        "value": "http://purl.org/adms/status/historicalArchive"
                    }
                ],
                "http://purl.org/dc/terms/description": [
                    {
                        "type": "literal",
                        "value": "Nedlastning gjennom Geonorge-portalen ved bruk av handlevognsfunksjonalitet"
                    }
                ],
                "http://purl.org/dc/terms/license": [
                    {
                        "type": "uri",
                        "value": "http://data.norge.no/nlod/no/1.0"
                    }
                ],
                "http://purl.org/dc/terms/title": [
                    {
                        "type": "literal",
                        "value": "Geonorge nedlastning",
                        "lang": "no"
                    }
                ]
            }
        }
    ]
    meta_data_list = [
        {"https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b7611952-9341-37a8-afcf-a1c5499805a5": {
            "http://xmlns.com/foaf/0.1/primaryTopic": [
                {
                    "type": "uri",
                    "value": "http://brreg.no/catalogs/910244132/datasets/17ed5a7d-1a22-49f4-a1d6-25f7d90dfa6d"
                }
            ],
            "http://purl.org/dc/terms/isPartOf": [
                {
                    "type": "uri",
                    "value": "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/821c273e-c4b0-3807-8d54-f54998747507"
                }
            ],
            "http://purl.org/dc/terms/identifier": [
                {
                    "type": "literal",
                    "value": "b7611952-9341-37a8-afcf-a1c5499805a5"
                }
            ],
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#CatalogRecord"
                }
            ]}},
        {"https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b12345-9876-ghg": {
            "http://xmlns.com/foaf/0.1/primaryTopic": [
                {
                    "type": "uri",
                    "value": "http://brreg.no/catalogs/910244132/datasets/987654-12hhhj-123"
                }
            ],
            "http://purl.org/dc/terms/isPartOf": [
                {
                    "type": "uri",
                    "value": "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/821c273e-c4b0-3807-8d54-f54998747507"
                }
            ],
            "http://purl.org/dc/terms/identifier": [
                {
                    "type": "literal",
                    "value": "b7611952-9341-37a8-afcf-a1c5499805a5"
                }
            ],
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#CatalogRecord"
                }
            ]}},
        {"https://datasets.staging.fellesdatakatalog.digdir.no/datasets/b1285678-jhj7p": {
            "http://xmlns.com/foaf/0.1/primaryTopic": [
                {
                    "type": "uri",
                    "value": "http://brreg.no/catalogs/910244132/datasets/987654-12hhhj-123-hkjh34-ah7"
                }
            ],
            "http://purl.org/dc/terms/isPartOf": [
                {
                    "type": "uri",
                    "value": "https://datasets.staging.fellesdatakatalog.digdir.no/catalogs/821c273e-c4b0-3807-8d54-f54998747507"
                }
            ],
            "http://purl.org/dc/terms/identifier": [
                {
                    "type": "literal",
                    "value": "b7611952-9341-37a8-afcf-a1c5499805a5"
                }
            ],
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [
                {
                    "type": "uri",
                    "value": "http://www.w3.org/ns/dcat#CatalogRecord"
                }
            ]}}
    ]
    result = merge_dataset_information(dataset=dataset_with_orgpath,
                                       distributions=distributions,
                                       records=meta_data_list)
    assert len(dataset_with_orgpath["http://www.w3.org/ns/dcat#distribution"]) == 3
    expected_dist_formats = ["SOSI", "GML", "HTML"]
    assert result["http://www.w3.org/ns/dcat#distribution"][0][JSON_LD.DCT.format][0]["value"] in expected_dist_formats
    assert result["http://www.w3.org/ns/dcat#distribution"][1][JSON_LD.DCT.format][0]["value"] in expected_dist_formats
    assert result["http://www.w3.org/ns/dcat#distribution"][2][JSON_LD.DCT.format][0]["value"] in expected_dist_formats
