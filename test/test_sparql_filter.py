import pytest

from src.sparql_utils.sparql_namespaces import DCT
from src.sparql_utils.sparql_query_builder import SparqlSelect, SparqlWhere, SparqlGraphTerm, SparqlFilter, \
    SparqlBuilder


@pytest.mark.unit
def test_string_filter():
    expected = "SELECT ?thing ?weight WHERE { ?thing dct:format ?weight . FILTER(?weight > 5 && ?weight < 7.0) } "
    select = SparqlSelect(variable_names=["thing", "weight"])
    where = SparqlWhere(
        graphs=[SparqlGraphTerm.build_graph_pattern(
            subject=SparqlGraphTerm(var="thing"),
            predicate=SparqlGraphTerm(namespace_property=DCT.format),
            obj=SparqlGraphTerm(var="weight"),
            close_pattern_with="."
        )],
        filters=[
            SparqlFilter(filter_string="?weight > 5 && ?weight < 7.0")
        ]
    )

    query = SparqlBuilder(select=select, where=where).build()
    assert query == expected


@pytest.mark.unit
def test_list_filter():
    expected = \
        "FILTER(?organization IN ('http://data.brreg.no/enhetsregisteret/enhet/971032082'," \
        "'http://data.brreg.no/enhetsregisteret/enhet/971032081'))"

    result = SparqlFilter(filter_on_var="organization",
                          filter_on_values=["http://data.brreg.no/enhetsregisteret/enhet/971032082",
                                            "http://data.brreg.no/enhetsregisteret/enhet/971032081"])

    assert str(result) == expected


@pytest.mark.unit
def test_collect_filters():
    expected = [
        SparqlFilter(filter_on_var="first", filter_on_values=["one", "two", "three"]),
        SparqlFilter(filter_on_var="second", filter_on_values=["two", "three", "one"]),
        SparqlFilter(filter_on_var="third", filter_on_values=["four", "twentytwo", "three"])
    ]

    result = SparqlFilter.collect_filters(first=["one", "two", "three"], second=["two", "three", "one"],
                                          third=["four", "twentytwo", "three"], aaaaand=None)
    assert len(result) == 3
    assert result[0].var == expected[0].var
    assert result[1].var == expected[1].var
    assert result[2].var == expected[2].var
