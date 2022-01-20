from typing import List, Optional

informationmodels = {
    "head": {"vars": ["record", "issued", "publisher"]},
    "results": {
        "bindings": [
            {
                "record": {
                    "type": "uri",
                    "value": "https://informationmodels.staging.fellesdatakatalog.digdir.no/informationmodels/90096759-a1e5-376a-a7e4-0e964266d3fc",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-11-26T09:24:02.192Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/oppslag/enheter/974761076",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://informationmodels.staging.fellesdatakatalog.digdir.no/informationmodels/60ecfff8-9ea3-41ee-92cc-7e791d73dac0",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-08-14T14:18:27Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://organization-catalogue.fellesdatakatalog.digdir.no/organizations/991825827",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://informationmodels.staging.fellesdatakatalog.digdir.no/informationmodels/a40bc112-f3bc-4c80-95d5-82986ab009b3",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-08-14T14:18:27Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://organization-catalogue.fellesdatakatalog.digdir.no/organizations/991825827",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://informationmodels.staging.fellesdatakatalog.digdir.no/informationmodels/5b15202c-ae33-35a5-aeaa-2692b9a75ec6",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-12-02T08:19:57.57Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://organization-catalogue.fellesdatakatalog.digdir.no/organizations/971040238",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://informationmodels.staging.fellesdatakatalog.digdir.no/informationmodels/6feff2b7-c7e5-3bde-99bf-9e5ae5cd6be8",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-12-02T08:35:16.054Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://organization-catalogue.staging.fellesdatakatalog.digdir.no/organizations/910258028",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://informationmodels.staging.fellesdatakatalog.digdir.no/informationmodels/a4207027-c476-37f6-84b0-0d5fc0555610",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-12-02T08:35:16.054Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://organization-catalogue.staging.fellesdatakatalog.digdir.no/organizations/910258028",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://informationmodels.staging.fellesdatakatalog.digdir.no/informationmodels/0bf6b09f-e1c0-3415-bba0-7ff2edada89d",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-11-26T09:24:14.599Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://raw.github.com/Informasjonsforvaltning/model-publisher/master/src/model/model-catalog.ttl#Utgiver",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://informationmodels.staging.fellesdatakatalog.digdir.no/informationmodels/bcbe6738-85f6-388c-afcc-ef1fafd7cc45",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-11-26T09:24:14.599Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://raw.github.com/Informasjonsforvaltning/model-publisher/master/src/model/model-catalog.ttl#Utgiver",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://informationmodels.staging.fellesdatakatalog.digdir.no/informationmodels/77ff9ff4-c6d7-3f84-91bd-c76bd6fad381",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2021-05-10T18:00:09.824Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://organization-catalogue.fellesdatakatalog.digdir.no/organizations/971526920",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://informationmodels.staging.fellesdatakatalog.digdir.no/informationmodels/665d7f6a-f6fd-3c6b-ade3-d3152ba171d1",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2021-02-01T08:46:40.305Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://organization-catalogue.fellesdatakatalog.digdir.no/organizations/915933149",
                },
            },
        ]
    },
}

concepts_in_use = {
    "_embedded": {
        "concepts": [
            {
                "id": "f635d5b4-c6f6-4fd0-8c7a-ceb9fea992ee",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/f635d5b4-c6f6-4fd0-8c7a-ceb9fea992ee",
                "prefLabel": {"nb": "etterregistrering"},
            },
            {
                "id": "5cd09fd8-0ac9-494a-b49e-3fa68ef9bb30",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/5cd09fd8-0ac9-494a-b49e-3fa68ef9bb30",
                "prefLabel": {"nb": "det alminnelige gruppeunntaket "},
            },
            {
                "id": "8d641622-9bb9-4316-b2ab-b27e083f893f",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/8d641622-9bb9-4316-b2ab-b27e083f893f",
                "prefLabel": {"nb": "arkivskaper", "en": "creator of archive"},
            },
        ]
    },
    "page": {"size": 10, "totalElements": 3769, "totalPages": 377, "number": 0},
}
concepts_aggregation = {
    "_embedded": {
        "concepts": [
            {
                "id": "a8ea479a-9b61-4cc2-86e8-650a03a322cc",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/a8ea479a-9b61-4cc2-86e8-650a03a322cc",
                "prefLabel": {"nb": "Behandling av personopplysning"},
            },
            {
                "id": "8831b4e0-66e4-4b3b-8136-0d982aec17a3",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/8831b4e0-66e4-4b3b-8136-0d982aec17a3",
                "prefLabel": {"nb": "Digital kontaktinformasjon"},
            },
            {
                "id": "03b58e56-3ba4-4d7d-9334-4cd23b629207",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/03b58e56-3ba4-4d7d-9334-4cd23b629207",
                "prefLabel": {"nb": "Kilde"},
            },
            {
                "id": "5d5932c8-43ca-454c-9dab-500f58b6bffd",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/5d5932c8-43ca-454c-9dab-500f58b6bffd",
                "prefLabel": {"nb": "Familierelasjon"},
            },
            {
                "id": "44c924de-b7f8-4dd1-87f1-7473034604d0",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/44c924de-b7f8-4dd1-87f1-7473034604d0",
                "prefLabel": {"nb": "Standardinnsats SPES"},
            },
            {
                "id": "85b3711b-02ad-4c3f-9d9e-67bc052ac205",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/85b3711b-02ad-4c3f-9d9e-67bc052ac205",
                "prefLabel": {"nb": "Pleiepenger SPES"},
            },
            {
                "id": "927a2453-d937-44c7-95bd-4b13b56eb996",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/927a2453-d937-44c7-95bd-4b13b56eb996",
                "prefLabel": {"nb": "Ansvar SPES"},
            },
            {
                "id": "046aaaae-0bee-46d6-82b5-40a898a12b63",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/046aaaae-0bee-46d6-82b5-40a898a12b63",
                "prefLabel": {
                    "nb": "skattepliktige som skal levere skattemelding til Sentralskattekontoret for utenlandssaker"
                },
            },
            {
                "id": "ed6c8e1b-ff55-4097-a0e7-56b8c86c532e",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/ed6c8e1b-ff55-4097-a0e7-56b8c86c532e",
                "prefLabel": {"nb": "saksopplysning"},
            },
            {
                "id": "3a5dc2d7-0198-4bdb-97ef-a3147d80dd3a",
                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/3a5dc2d7-0198-4bdb-97ef-a3147d80dd3a",
                "prefLabel": {
                    "nb": "vurderes for skattebegrensning paragraf 17 liten skatteevne"
                },
            },
        ]
    },
    "page": {"size": 10, "totalElements": 4267, "totalPages": 427, "number": 0},
    "aggregations": {
        "orgPath": {
            "buckets": [
                {"key": "/STAT", "count": 4224},
                {"key": "/STAT/972417807", "count": 3386},
                {"key": "/STAT/972417807/974761076", "count": 3386},
                {"key": "/STAT/983887457", "count": 568},
                {"key": "/STAT/983887457/889640782", "count": 568},
                {"key": "/STAT/912660680", "count": 270},
                {"key": "/STAT/912660680/974760673", "count": 270},
                {"key": "/ANNET", "count": 43},
                {"key": "/ANNET/910298062", "count": 21},
                {"key": "/ANNET/910244132", "count": 17},
                {"key": "/ANNET/910258028", "count": 5},
            ]
        },
        "firstHarvested": {
            "buckets": [
                {"key": "last30days", "count": 96},
                {"key": "last365days", "count": 4267},
                {"key": "last7days", "count": 10},
            ]
        },
    },
}
concepts_response = {
    "head": {"vars": ["record", "issued", "publisher"]},
    "results": {
        "bindings": [
            {
                "record": {
                    "type": "uri",
                    "value": "https://concepts.staging.fellesdatakatalog.digdir.no/concepts/41cd33fc-c34e-4473-a963-bc56fe01ac91",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-07-03T10:49:41.625Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974761076",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://concepts.staging.fellesdatakatalog.digdir.no/concepts/c162be91-dc94-4122-96b4-c082ccdc130b",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-07-03T11:10:43.255Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://concepts.staging.fellesdatakatalog.digdir.no/concepts/cc26db3c-1858-4c95-8221-5161cd088c30",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-07-03T11:12:13.688Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://concepts.staging.fellesdatakatalog.digdir.no/concepts/c2fac930-2b20-4d40-80ea-972fd8678d80",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-11-27T12:00:14.086Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://concepts.staging.fellesdatakatalog.digdir.no/concepts/8cf3567a-a91a-47ff-bd0e-ec4b34b74b77",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-07-03T10:29:34.845Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974761076",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://concepts.staging.fellesdatakatalog.digdir.no/concepts/212238a7-bfe1-4deb-9816-ebcd49a3619e",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2021-05-05T07:27:20.086Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974761076",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://concepts.staging.fellesdatakatalog.digdir.no/concepts/cfe95c10-38d0-42dd-aa5b-441ea58d72a3",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-07-03T10:10:15.424Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974761076",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://concepts.staging.fellesdatakatalog.digdir.no/concepts/8a64668e-16d2-485f-abf2-0444c8055b43",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-07-03T11:03:34.969Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974761076",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://concepts.staging.fellesdatakatalog.digdir.no/concepts/50dfe540-41b1-352f-869e-292c03999fc7",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2021-05-25T14:58:13.767Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/910244132",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://concepts.staging.fellesdatakatalog.digdir.no/concepts/06cc8a71-748f-43d2-8208-217116bba88d",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-07-03T10:06:21.949Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/974761076",
                },
            },
            {
                "record": {
                    "type": "uri",
                    "value": "https://concepts.staging.fellesdatakatalog.digdir.no/concepts/b10cdab3-e679-46f3-9d1d-8caaef24f098",
                },
                "issued": {
                    "type": "literal",
                    "datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "value": "2020-07-03T09:57:35.995Z",
                },
                "publisher": {
                    "type": "uri",
                    "value": "https://data.brreg.no/enhetsregisteret/api/enheter/910244132",
                },
            },
        ]
    },
}

mocked_organization_catalog_response = [
    {
        "organizationId": "974760673",
        "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/974760673",
        "internationalRegistry": None,
        "name": "REGISTERENHETEN I BRØNNØYSUND",
        "orgType": "ORGL",
        "orgPath": "/STAT/912660680/974760673",
        "subOrganizationOf": "912660680",
        "issued": "1995-08-09",
        "municipalityNumber": "1813",
        "industryCode": "84.110",
        "sectorCode": "6100",
        "prefLabel": None,
        "allowDelegatedRegistration": None,
    },
    {
        "organizationId": "991825827",
        "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/991825827",
        "internationalRegistry": None,
        "name": "Digitaliseringsdirektoratet",
        "orgType": "ORGL",
        "orgPath": "/STAT/972417858/991825827",
        "subOrganizationOf": "972417858",
        "issued": "2007-10-15",
        "municipalityNumber": "0301",
        "industryCode": "84.110",
        "sectorCode": "6100",
        "prefLabel": {
            "nb": "Digitaliseringsdirektoratet",
            "nn": "Digitaliseringsdirektoratet",
            "en": "Norwegian Digitalisation Agency",
        },
        "allowDelegatedRegistration": None,
    },
    {
        "organizationId": "917422575",
        "norwegianRegistry": "https://data.brreg.no/enhetsregisteret/api/enheter/917422575",
        "internationalRegistry": None,
        "name": "ENTUR AS",
        "orgType": "AS",
        "orgPath": "/PRIVAT/917422575",
        "subOrganizationOf": None,
        "issued": "2016-07-04",
        "municipalityNumber": "0301",
        "industryCode": "62.010",
        "sectorCode": "1120",
        "prefLabel": None,
        "allowDelegatedRegistration": None,
    },
]


def mocked_access_rights(uri: str) -> Optional[str]:
    if (
        uri
        == "<http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC>"
    ):
        return "NON_PUBLIC"
    elif (
        uri == "<http://publications.europa.eu/resource/authority/access-right/PUBLIC>"
    ):
        return "PUBLIC"
    elif (
        uri
        == "<http://publications.europa.eu/resource/authority/access-right/RESTRICTED>"
    ):
        return "RESTRICTED"
    else:
        return None


def mocked_org_paths(uri: str, name: str, **args):
    if uri == "<https://data.brreg.no/enhetsregisteret/api/enheter/974760673>":
        return "/STAT/912660680/974760673"
    elif uri == "<https://data.brreg.no/enhetsregisteret/api/enheter/991825827>":
        return "/STAT/972417858/991825827"
    elif uri == "<https://data.brreg.no/enhetsregisteret/api/enheter/917422575>":
        return "/STAT/912660680/917422575"
    else:
        return f"/ANNET{name}"


def mocked_los_paths(uri: str) -> Optional[List[str]]:
    if (
        uri
        == "http://objektkatalog.geonorge.no/Objekttype/Index/EAID_EDD3FB30_A0A2_4ced_B367_5C4A5979F676"
    ):
        return None
    paths = {
        "https://psi.norge.no/los/tema/bygg-og-eiendom": ["bygg-og-eiendom"],
        "https://psi.norge.no/los/tema/priser-og-gebyr-for-bygg-og-eiendom": [
            "bygg-og-eiendom/priser-og-gebyr-for-bygg-og-eiendom",
            "natur-klima-og-miljo/avfallshandtering/kompostering",
        ],
        "https://psi.norge.no/los/ord/renovasjonsavgift": [
            "bygg-og-eiendom/priser-og-gebyr-for-bygg-og-eiendom/renovasjonsavgift"
        ],
        "https://psi.norge.no/los/ord/kompostering": [
            "natur-klima-og-miljo/avfallshandtering/kompostering"
        ],
    }
    return paths[uri]


def mock_access_rights_catalog_response():
    return [
        {
            "uri": "http://publications.europa.eu/resource/authority/access-right",
            "prefLabel": {"en": "Access right Named Authority List"},
        },
        {
            "uri": "http://publications.europa.eu/resource/authority/access-right/NON_PUBLIC",
            "code": "NON_PUBLIC",
            "prefLabel": {
                "nn": "Ikke-offentlig",
                "nb": "Ikke-offentlig",
                "en": "Non-public",
            },
        },
        {
            "uri": "http://publications.europa.eu/resource/authority/access-right/PUBLIC",
            "code": "PUBLIC",
            "prefLabel": {"en": "Public", "nb": "Offentlig", "nn": "Offentlig"},
        },
        {
            "uri": "http://publications.europa.eu/resource/authority/access-right/RESTRICTED",
            "code": "RESTRICTED",
            "prefLabel": {"nb": "Begrenset", "nn": "Begrenset", "en": "Restricted"},
        },
    ]


def mock_los_path_reference_response():
    return [
        {
            "internalId": None,
            "children": None,
            "parents": ["https://psi.norge.no/los/tema/kultur"],
            "isTheme": False,
            "losPaths": ["kultur-idrett-og-fritid/kultur/festival"],
            "name": {"nn": "Festival", "nb": "Festival", "en": "Festivals"},
            "definition": None,
            "uri": "https://psi.norge.no/los/ord/festival",
            "synonyms": ["Billettbestilling", "Festivalpass"],
            "relatedTerms": None,
            "tema": False,
        },
        {
            "internalId": None,
            "children": [
                "https://psi.norge.no/los/ord/renovasjonsavgift",
                "https://psi.norge.no/los/ord/eiendomsskatt",
                "https://psi.norge.no/los/ord/gebyr-for-byggesak",
                "https://psi.norge.no/los/ord/betalingssatser-for-kommunale-tjenester",
            ],
            "parents": ["https://psi.norge.no/los/tema/bygg-og-eiendom"],
            "isTheme": True,
            "losPaths": ["bygg-og-eiendom/priser-og-gebyr-for-bygg-og-eiendom"],
            "name": {
                "nn": "Prisar og gebyr for bygg og eigedom",
                "nb": "Priser og gebyr for bygg og eiendom",
                "en": "Prices and fees for construction and property",
            },
            "definition": None,
            "uri": "https://psi.norge.no/los/tema/priser-og-gebyr-for-bygg-og-eiendom",
            "synonyms": [],
            "relatedTerms": None,
            "tema": True,
        },
        {
            "internalId": None,
            "children": None,
            "parents": [
                "https://psi.norge.no/los/tema/kjop-og-salg",
                "https://psi.norge.no/los/tema/okonomiske-ytelser-og-radgivning",
            ],
            "isTheme": False,
            "losPaths": [
                "bygg-og-eiendom/kjop-og-salg/boligfinansiering",
                "sosiale-tjenester/okonomiske-ytelser-og-radgivning/boligfinansiering",
            ],
            "name": {
                "nn": "Bustadfinansiering",
                "nb": "Boligfinansiering",
                "en": "Home financing",
            },
            "definition": None,
            "uri": "https://psi.norge.no/los/ord/boligfinansiering",
            "synonyms": [
                "Startlån",
                "Etableringstilskot",
                "Grunnlån",
                "Huslån",
                "Bustadlån",
                "Husbanken",
                "Utbetringslån",
                "Utbedringslån",
                "Boligtilskudd",
                "Etableringstilskudd",
                "Byggelån",
                "Bustadtilskot",
                "Boliglån",
            ],
            "relatedTerms": [
                "https://psi.norge.no/los/ord/eiendomsomsetning",
                "https://psi.norge.no/los/ord/forhandskonferanse",
                "https://psi.norge.no/los/ord/bostotte",
                "https://psi.norge.no/los/ord/okonomisk-radgiving",
                "https://psi.norge.no/los/ord/byggesak",
            ],
            "tema": False,
        },
        {
            "internalId": None,
            "children": None,
            "parents": ["https://psi.norge.no/los/tema/barnevern-og-foreldrestotte"],
            "isTheme": False,
            "losPaths": [
                "familie-og-barn/barnevern-og-foreldrestotte/bekymringsmelding-til-barnevernet"
            ],
            "name": {
                "nn": "Melding til barnevernstenesta",
                "nb": "Bekymringsmelding til barnevernet",
                "en": "Reports to the child welfare service",
            },
            "definition": None,
            "uri": "https://psi.norge.no/los/ord/bekymringsmelding-til-barnevernet",
            "synonyms": [],
            "relatedTerms": None,
            "tema": False,
        },
        {
            "internalId": None,
            "children": None,
            "parents": ["https://psi.norge.no/los/tema/innbyggerrettigheter"],
            "isTheme": False,
            "losPaths": [
                "demokrati-og-innbyggerrettigheter/innbyggerrettigheter/pass-og-visum"
            ],
            "name": {
                "nn": "Pass og visum",
                "nb": "Pass og visum",
                "en": "Passports and visa",
            },
            "definition": None,
            "uri": "https://psi.norge.no/los/ord/pass-og-visum",
            "synonyms": [
                "Legitimasjon",
                "Reisedokument",
                "Reisebevis",
                "Schengen-avtalen",
                "Utlendingspass",
                "Reiseløyve",
            ],
            "relatedTerms": ["https://psi.norge.no/los/hendelse/fa-barn"],
            "tema": False,
        },
    ]
