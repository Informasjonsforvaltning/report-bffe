def get_dataset_publisher_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?name ?publisher ?sameAs
        FROM <https://datasets.fellesdatakatalog.digdir.no>
        WHERE {{
            ?subject dct:publisher ?publisher .
            ?publisher foaf:name ?name .
            OPTIONAL {{
                ?publisher owl:sameAs ?sameAs .
            }}
        }}
    """


def get_dataservice_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?record ?publisher ?issued ?sameAs ?mediaType
        FROM <https://dataservices.fellesdatakatalog.digdir.no>
        WHERE {{
            ?catalog a dcat:Catalog .
            ?catalog dct:publisher ?publisher .
            ?catalog dcat:service ?service .
            ?record foaf:primaryTopic ?service .
            ?record dct:issued ?issued .
            OPTIONAL {{
                ?publisher owl:sameAs ?sameAs .
                ?service dcat:mediaType ?mediaType .
            }}
        }}
    """


def get_dataservice_publisher_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?publisher ?sameAs
        FROM <https://dataservices.fellesdatakatalog.digdir.no>
        WHERE {{
            ?subject dct:publisher ?publisher .
            OPTIONAL {{
                ?publisher owl:sameAs ?sameAs .
            }}
        }}
    """


def get_concepts_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT DISTINCT ?record ?issued ?publisher
        FROM <https://concepts.fellesdatakatalog.digdir.no>
        WHERE {{
            ?concept a skos:Concept .
            ?record foaf:primaryTopic ?concept .
            ?record dct:issued ?issued .
            ?collection skos:member ?concept .
            OPTIONAL {{ ?concept dct:publisher ?conceptPublisher . }}
            OPTIONAL {{ ?collection dct:publisher ?collectionPublisher . }}
            BIND ( IF( EXISTS {{ ?concept dct:publisher ?conceptPublisher . }},
                ?conceptPublisher, ?collectionPublisher ) AS ?publisher ) .
        }}
    """


def get_concept_publishers_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?publisher ?sameAs
        FROM <https://concepts.fellesdatakatalog.digdir.no>
        WHERE {{
            ?subject dct:publisher ?publisher .
            OPTIONAL {{
                ?publisher owl:sameAs ?sameAs .
            }}
        }}
    """


def get_info_models_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#>
        SELECT DISTINCT ?record ?issued ?publisher
        FROM <https://informationmodels.fellesdatakatalog.digdir.no>
        WHERE {{
            ?informationmodel a modelldcatno:InformationModel .
            ?record foaf:primaryTopic ?informationmodel .
            ?record dct:issued ?issued .
            ?catalog modelldcatno:model ?informationmodel .
            OPTIONAL {{ ?informationmodel dct:publisher ?informationmodelPublisher . }}
            OPTIONAL {{ ?catalog dct:publisher ?catalogPublisher . }}
            BIND ( IF( EXISTS {{ ?informationmodel dct:publisher ?informationmodelPublisher . }},
                ?informationmodelPublisher, ?catalogPublisher ) AS ?publisher ) .
        }}
    """


def get_info_model_publishers_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?publisher ?sameAs
        FROM <https://informationmodels.fellesdatakatalog.digdir.no>
        WHERE {{
            ?subject dct:publisher ?publisher .
            OPTIONAL {{
                ?publisher owl:sameAs ?sameAs .
            }}
        }}
    """
