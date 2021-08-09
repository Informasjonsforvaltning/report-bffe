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
