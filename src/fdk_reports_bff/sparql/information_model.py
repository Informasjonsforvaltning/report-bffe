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
