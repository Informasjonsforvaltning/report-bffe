def get_dataservice_query() -> str:
    return """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX br: <https://raw.githubusercontent.com/Informasjonsforvaltning/organization-catalog/main/src/main/resources/ontology/organization-catalog.owl#>
SELECT DISTINCT ?record ?publisher ?firstHarvested ?mediaType ?format ?orgId ?orgPath
FROM <https://dataservices.fellesdatakatalog.digdir.no>
WHERE {
  ?service a dcat:DataService .
  ?record foaf:primaryTopic ?service .
  ?record a dcat:CatalogRecord .
  ?record dct:issued ?firstHarvested .
  OPTIONAL { ?service dcat:mediaType ?mediaType . }
  OPTIONAL { ?service dct:format ?format . }
  OPTIONAL {
    ?service dct:publisher ?publisher .
    ?publisher dct:identifier ?orgId .
    ?publisher br:orgPath ?orgPath .
  }
}"""


def dataservice_timeseries_datapoint_query() -> str:
    return """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX br: <https://raw.githubusercontent.com/Informasjonsforvaltning/organization-catalog/main/src/main/resources/ontology/organization-catalog.owl#>
SELECT DISTINCT ?service ?orgPath
WHERE {
  ?service a dcat:DataService .
  ?record foaf:primaryTopic ?service .
  ?record a dcat:CatalogRecord .
  OPTIONAL {
    ?service dct:publisher ?publisher .
    ?publisher br:orgPath ?orgPath .
  }
}"""
