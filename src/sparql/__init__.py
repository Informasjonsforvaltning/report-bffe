def get_dataset_publisher_query():
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?name ?publisher ?sameAs
        FROM <https://datasets.fellesdatakatalog.digdir.no>
        WHERE {{
            ?publisher a foaf:Agent .
            ?publisher foaf:name ?name .
            OPTIONAL {{ ?publisher owl:sameAs ?sameAs }}
        }}
        GROUP BY ?name ?publisher ?sameAs
    """


def get_dataservice_query():
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
                ?service dcat:mediaType ?mediaType
            }}
        }}
    """


def get_dataservice_publisher_query():
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?publisher ?sameAs
        FROM <https://dataservices.fellesdatakatalog.digdir.no>
        WHERE {{
            ?publisher a foaf:Agent .
            OPTIONAL {{ ?publisher owl:sameAs ?sameAs }}
        }}
        GROUP BY ?publisher ?sameAs
    """
