import pytest

from src.sparql_utils.sparql_namespaces import DCT, NamespaceProperty, FOAF, SparqlFunctionString
from src.sparql_utils.sparql_query_builder import SparqlCount, SparqlGraphPatternTerm, SparqlFunction, \
    SparqlSelect, SparqlWhere


@pytest.mark.unit
def test_simple_select():
    expected = "SELECT ?some ?vars ?to"
    result = SparqlSelect(variable_names=["some", "vars", "to"]).__str__()
    assert expected == result


@pytest.mark.unit
def test_select_all():
    expected = "SELECT *"
    result = SparqlSelect().__str__()
    assert expected == result


@pytest.mark.unit
def test_build_count():
    expected_default = "(COUNT(?format) AS ?count)"
    default_result = SparqlCount("format")
    assert default_result.__str__() == expected_default
    expected = "(COUNT(?id) AS ?org_count)"
    result = SparqlCount("id", "org_count")
    assert result.__str__() == expected


@pytest.mark.unit
def test_select_with_count():
    expected = "SELECT (COUNT(?format) AS ?format_count)"
    count = SparqlCount("format", "format_count")
    result = SparqlSelect(count_variables=[count]).__str__()
    assert result == expected


@pytest.mark.unit
def test_select_variables_and_count():
    expected = "SELECT ?name (COUNT(?d1) AS ?withSubject) (COUNT(?d2) AS ?openData)"
    result = SparqlSelect(
        variable_names=["name"],
        count_variables=[SparqlCount("d1", "withSubject"), SparqlCount("d2", "openData")]
    ).__str__()
    assert result == expected


@pytest.mark.unit
def test_build_graph_pattern():
    expected = "?distribution dct:format ?distributionFormat ."
    result = SparqlGraphPatternTerm.build_graph_pattern(
        subject=SparqlGraphPatternTerm(var="distribution"),
        predicate=SparqlGraphPatternTerm(namespace_property=DCT.format),
        obj=SparqlGraphPatternTerm(var="distributionFormat"),
        close_pattern_with="."
    )

    assert result == expected


@pytest.mark.unit
def test_build_type_graph_pattern():
    expected = "?publisher a foaf:Agent ."
    result = SparqlGraphPatternTerm.build_graph_pattern(
        subject=SparqlGraphPatternTerm(var="publisher"),
        predicate=SparqlGraphPatternTerm(namespace_property=NamespaceProperty.RDF_TYPE),
        obj=SparqlGraphPatternTerm(namespace_property=FOAF.agent),
        close_pattern_with="."
    )

    assert result == expected


@pytest.mark.unit
def test_build_lcase_function():
    expected = "LCASE(?distributionFormat) AS ?format"
    result = SparqlFunction.build_string(fun=SparqlFunctionString.LCASE, variable="distributionFormat",
                                         as_name="format")
    assert result == expected


@pytest.mark.unit
def test_build_function_with_args():
    expected = "STR(?accessRights), '^.*\\/', '')"
    result = SparqlFunction.build_string(fun=SparqlFunctionString.STR, variable="accessRights", args=['^.*\\/', ''])
    assert result == expected


@pytest.mark.unit
def test_str_with_inner_function():
    expected = "REPLACE(STR(?accessRights), '^.*\\/', '')"
    inner_fun = "STR(?accessRights), '^.*\\/', ''"
    assert SparqlFunction(fun=SparqlFunctionString.REPLACE).str_with_inner_function(inner_fun) == expected


@pytest.mark.unit
def test_str_with_inner_function_with_as_name():
    expected = "REPLACE(STR(?accessRights), '^.*\\/', '') AS ?code"
    inner_fun = "STR(?accessRights), '^.*\\/', ''"
    assert SparqlFunction(fun=SparqlFunctionString.REPLACE, as_name="code").str_with_inner_function(
        inner_fun) == expected


@pytest.mark.unit
def test_function_str_from_hierarchy():
    expected = "BIND(REPLACE(STR(?accessRights), '^.*\\/', '') AS ?code)"
    root = SparqlFunction(fun=SparqlFunctionString.BIND)
    first_child = SparqlFunction(fun=SparqlFunctionString.REPLACE, as_name="code", parent=root)
    leaf = SparqlFunction(fun=SparqlFunctionString.STR,
                          variable="accessRights",
                          args=['^.*\\/', ''],
                          parent=first_child
                          )

    result = SparqlFunction.str_from_hierarchy(leaf)
    assert result == expected


@pytest.mark.unit
def test_build_simple_where():
    expected = "WHERE { ?distribution dct:format ?distributionFormat . } "

    graph = SparqlGraphPatternTerm.build_graph_pattern(
        subject=SparqlGraphPatternTerm(var="distribution"),
        predicate=SparqlGraphPatternTerm(namespace_property=DCT.format),
        obj=SparqlGraphPatternTerm(var="distributionFormat"),
        close_pattern_with="."
    )
    result = SparqlWhere(graphs=[graph])

    assert str(result) == expected


@pytest.mark.unit
def test_build_where_with_function():
    expected = "WHERE { BIND(LCASE(?distributionFormat) AS ?format) } "
    root_function = SparqlFunction(fun=SparqlFunctionString.BIND)
    leaf = SparqlFunction(fun=SparqlFunctionString.LCASE,
                          variable="distributionFormat",
                          as_name="format",
                          parent=root_function)
    result = SparqlWhere(functions=[leaf])

    assert str(result) == expected


@pytest.mark.unit
def test_build_simple_where():
    expected = "WHERE { ?distribution dct:format ?distributionFormat . BIND(LCASE(?distributionFormat) AS ?format) } "

    graph = SparqlGraphPatternTerm.build_graph_pattern(
        subject=SparqlGraphPatternTerm(var="distribution"),
        predicate=SparqlGraphPatternTerm(namespace_property=DCT.format),
        obj=SparqlGraphPatternTerm(var="distributionFormat"),
        close_pattern_with="."
    )

    leaf = SparqlFunction(fun=SparqlFunctionString.LCASE,
                          variable="distributionFormat",
                          as_name="format",
                          parent=SparqlFunction(fun=SparqlFunctionString.BIND))

    result = SparqlWhere(graphs=[graph], functions=[leaf])

    assert str(result) == expected


@pytest.mark.unit
def test_mk():
    expected = "PREFIX dct: <http://purl.org/dc/terms/> " \
               "SELECT ?format (COUNT(?format) AS ?count) " \
               "WHERE { " \
               "?distribution dct:format ?distributionFormat . BIND(LCASE(?distributionFormat) AS ?format) } " \
               "GROUP BY ?format" \
               "ORDER BY DESC(?count)"
