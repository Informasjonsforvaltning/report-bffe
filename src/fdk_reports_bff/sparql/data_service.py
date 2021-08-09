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
