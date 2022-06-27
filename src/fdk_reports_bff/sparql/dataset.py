def get_datasets_query() -> str:
    return """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX fdk: <https://raw.githubusercontent.com/Informasjonsforvaltning/fdk-reasoning-service/main/src/main/resources/ontology/fdk.owl#>
        PREFIX br: <https://raw.githubusercontent.com/Informasjonsforvaltning/organization-catalog/main/src/main/resources/ontology/organization-catalog.owl#>
        SELECT DISTINCT ?catalog ?catalogTitle ?dataset ?record ?title ?firstHarvested ?theme ?accessRights ?provenance ?subject ?isOpenData ?mediaType ?format ?publisher ?orgId ?orgPath
        FROM <https://datasets.fellesdatakatalog.digdir.no>
        WHERE {
            ?catalog a dcat:Catalog .
            OPTIONAL { ?catalog dct:title ?catalogTitle . }
            ?catalog dcat:dataset ?dataset .

            ?record foaf:primaryTopic ?dataset .
            ?record dct:issued ?firstHarvested .

            OPTIONAL { ?dataset dct:title ?title . }
            OPTIONAL { ?dataset dcat:theme ?theme . }
            OPTIONAL { ?dataset dct:accessRights ?accessRights . }
            OPTIONAL { ?dataset dct:provenance ?provenance . }
            OPTIONAL { ?dataset dct:subject ?subject . }
            OPTIONAL { ?dataset fdk:isOpenData ?isOpenData . }

            OPTIONAL { ?dataset dcat:distribution ?distribution . }
            OPTIONAL { ?distribution dcat:mediaType ?mediaType . }
            OPTIONAL { ?distribution dct:format ?format . }

            OPTIONAL { ?dataset dct:publisher ?publisher . }
            OPTIONAL { ?publisher dct:identifier ?orgId . }
            OPTIONAL { ?publisher br:orgPath ?orgPath . }
        }"""
