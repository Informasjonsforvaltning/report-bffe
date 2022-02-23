def get_info_models_query() -> str:
    return """
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#>
        PREFIX br: <https://raw.githubusercontent.com/Informasjonsforvaltning/organization-catalog/master/src/main/resources/ontology/organization-catalog.owl#>
        SELECT DISTINCT ?record ?issued ?publisher ?orgId ?orgPath
        FROM <https://informationmodels.fellesdatakatalog.digdir.no>
        WHERE {{
            ?informationmodel a modelldcatno:InformationModel .
            ?record foaf:primaryTopic ?informationmodel .
            ?record dct:issued ?issued .
            ?catalog modelldcatno:model ?informationmodel .
            OPTIONAL {{ ?informationmodel dct:publisher ?publisher . }}
            OPTIONAL {{ ?publisher dct:identifier ?orgId . }}
            OPTIONAL {{ ?publisher br:orgPath ?orgPath . }}
        }}
    """
