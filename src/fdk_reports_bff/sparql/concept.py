def get_concepts_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX br: <https://raw.githubusercontent.com/Informasjonsforvaltning/organization-catalog/master/src/main/resources/ontology/organization-catalog.owl#>
        SELECT DISTINCT ?record ?issued ?publisher ?orgId ?orgPath
        FROM <https://concepts.fellesdatakatalog.digdir.no>
        WHERE {{
            ?concept a skos:Concept .
            ?record foaf:primaryTopic ?concept .
            ?record dct:issued ?issued .
            ?collection skos:member ?concept .
            OPTIONAL {{ ?concept dct:publisher ?publisher . }}
            OPTIONAL {{ ?publisher dct:identifier ?orgId . }}
            OPTIONAL {{ ?publisher br:orgPath ?orgPath . }}
        }}
    """
