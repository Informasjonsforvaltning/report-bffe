import pytest

from src.sparql_utils.sparql_namespaces import DCT, NamespaceProperty, FOAF, SparqlFunctionString
from src.sparql_utils.sparql_query_builder import SparqlBuilder, SparqlCount, SparqlGraphPatternTerm, SparqlFunction, \
    SparqlNestedFunction


@pytest.mark.unit
def test_simple_select():
    expected = "SELECT ?some ?vars ?to"
    result = SparqlBuilder.select(variable_names=["some", "vars", "to"])
    assert expected == result


@pytest.mark.unit
def test_select_all():
    expected = "SELECT *"
    result = SparqlBuilder.select()
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
    result = SparqlBuilder.select(count_variables=[count])
    assert result == expected


@pytest.mark.unit
def test_select_variables_and_count():
    expected = "SELECT ?name (COUNT(?d1) AS ?withSubject) (COUNT(?d2) AS ?openData)"
    result = SparqlBuilder.select(
        variable_names=["name"],
        count_variables=[SparqlCount("d1", "withSubject"), SparqlCount("d2", "openData")]
    )
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
def test_str_from_hierarchy():
    expected = "BIND(REPLACE(STR(?accessRights), '^.*\\/', '') AS ?code)"
    root = SparqlNestedFunction(parent=None, node=SparqlFunction(fun=SparqlFunctionString.BIND))
    first_child = SparqlNestedFunction(parent=root,
                                       node=SparqlFunction(fun=SparqlFunctionString.REPLACE, as_name="code"))
    leaf = SparqlNestedFunction(parent=first_child,
                                node=SparqlFunction(fun=SparqlFunctionString.STR, variable="accessRights",
                                                    args=['^.*\\/', '']))

    result = SparqlNestedFunction.str_from_hierarchy(leaf)
    assert result == expected
