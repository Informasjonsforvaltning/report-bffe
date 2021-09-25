def get_dataservice_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?record ?publisher ?issued ?sameAs ?mediaType ?format
        FROM <https://dataservices.fellesdatakatalog.digdir.no>
        WHERE {{
            ?catalog a dcat:Catalog .
            ?catalog dcat:service ?service .
            ?record foaf:primaryTopic ?service .
            ?record dct:issued ?issued .
            OPTIONAL {{ ?service dct:publisher ?servicePublisher . }}
            OPTIONAL {{ ?catalog dct:publisher ?catPublisher . }}
            BIND ( IF( EXISTS {{ ?service dct:publisher ?servicePublisher . }},
                ?servicePublisher, ?catPublisher ) AS ?publisher ) .
            OPTIONAL {{ ?publisher owl:sameAs ?sameAs . }}
            OPTIONAL {{ ?service dcat:mediaType ?mediaType . }}
            OPTIONAL {{ ?service dct:format ?format . }}
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
