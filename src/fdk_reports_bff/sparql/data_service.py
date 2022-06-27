def get_dataservice_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX br: <https://raw.githubusercontent.com/Informasjonsforvaltning/organization-catalog/main/src/main/resources/ontology/organization-catalog.owl#>
        SELECT ?record ?publisher ?firstHarvested ?mediaType ?format ?orgId ?orgPath
        FROM <https://dataservices.fellesdatakatalog.digdir.no>
        WHERE {{
            ?catalog a dcat:Catalog .
            ?catalog dcat:service ?service .
            ?record foaf:primaryTopic ?service .
            ?record dct:issued ?firstHarvested .
            OPTIONAL {{ ?service dct:publisher ?publisher . }}
            OPTIONAL {{ ?publisher dct:identifier ?orgId . }}
            OPTIONAL {{ ?publisher br:orgPath ?orgPath . }}
            OPTIONAL {{ ?service dcat:mediaType ?mediaType . }}
            OPTIONAL {{ ?service dct:format ?format . }}
        }}
    """
