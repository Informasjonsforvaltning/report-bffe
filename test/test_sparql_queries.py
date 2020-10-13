from src.sparql.queries import build_dataset_publisher_query


def test_build_dataset_publisher_query():
    expected = (
        "PREFIX dct: <http://purl.org/dc/terms/> PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX owl: "
        "<http://www.w3.org/2002/07/owl%23> SELECT ?name ?publisher ?sameAs WHERE { ?publisher a foaf:Agent . "
        "?publisher foaf:name ?name . OPTIONAL { ?publisher owl:sameAs "
        "?sameAs . }   } GROUP BY ?name ?publisher ?sameAs  "
    )

    result = build_dataset_publisher_query()
    assert result == expected
