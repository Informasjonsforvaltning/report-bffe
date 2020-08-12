from src.sparql_utils.sparql_namespaces import DCT, FOAF, OWL, NamespaceProperty, SparqlFunctionString, RDF
from src.sparql_utils.sparql_query_builder import SparqlSelect, SparqlCount, SparqlWhere, SparqlGraphTerm, \
    SparqlFunction, SparqlBuilder, SparqlOptional, encode_for_sparql


def build_datasets_catalog_query() -> str:
    prefixes = [DCT, FOAF, OWL]
    group_by = "organization"
    select_clause = SparqlSelect(variable_names=[group_by],
                                 count_variables=[SparqlCount(variable_name="item", as_name="count")]
                                 )
    where_clause = catalog_query_where_clause()

    query = SparqlBuilder(
        prefix=prefixes,
        select=select_clause,
        where=where_clause,
        group_by_var=group_by
    ).build()

    return encode_for_sparql(query)


def catalog_query_where_clause():
    bind_root = SparqlFunction(fun=SparqlFunctionString.BIND).str_with_inner_function("COALESCE(?sameAs, STR("
                                                                                      "?publisher)) AS ?organization")

    publisher_a_foaf_a_agent = SparqlGraphTerm.build_graph_pattern(
        subject=SparqlGraphTerm(var="publisher"),
        predicate=SparqlGraphTerm(namespace_property=RDF.TYPE),
        obj=SparqlGraphTerm(namespace_property=FOAF.agent),
        close_pattern_with="."
    )
    graph_patterns = [
        publisher_a_foaf_a_agent,
        SparqlGraphTerm.build_graph_pattern(
            subject=SparqlGraphTerm(var="item"),
            predicate=SparqlGraphTerm(namespace_property=DCT.publisher),
            obj=SparqlGraphTerm(var="publisher"),
            close_pattern_with="."
        )
    ]
    nested_select_clause = SparqlSelect(variable_names=["publisher", "organization"])
    nested_where = SparqlWhere(
        graphs=[publisher_a_foaf_a_agent],
        functions=[bind_root],
        optional=SparqlOptional(graphs=[
            SparqlGraphTerm.build_graph_pattern(
                subject=SparqlGraphTerm(var="publisher"),
                predicate=SparqlGraphTerm(namespace_property=OWL.sameAs),
                obj=SparqlGraphTerm(var="sameAs"),
                close_pattern_with="."
            )
        ])
    )
    nested_builder = SparqlBuilder(select=nested_select_clause, where=nested_where)

    return SparqlWhere(graphs=graph_patterns, nested_clause=nested_builder)
