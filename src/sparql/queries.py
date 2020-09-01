from src.rdf_namespaces import NamespaceProperty, DCT, FOAF, OWL, RDF, ContentKeys
from src.sparql.builder import SparqlSelect, SparqlWhere, SparqlGraphTerm, SparqlOptional, SparqlBuilder


def build_dataset_publisher_query():
    dct = DCT(NamespaceProperty.TTL)
    foaf = FOAF(NamespaceProperty.TTL)
    owl = OWL(NamespaceProperty.TTL)
    rdf = RDF(NamespaceProperty.TTL)
    prefixes = [dct, foaf, owl]
    name_var = ContentKeys.ORG_NAME
    publisher = ContentKeys.PUBLISHER
    publisher_graph_term = SparqlGraphTerm(var=publisher)
    sameAs = ContentKeys.SAME_AS
    select = SparqlSelect(variable_names=[name_var, publisher, sameAs])
    publisher_a_fof_agent = SparqlGraphTerm.build_graph_pattern(
        subject=publisher_graph_term,
        predicate=SparqlGraphTerm(namespace_property=rdf.type),
        obj=SparqlGraphTerm(namespace_property=foaf.agent),
        close_pattern_with="."
    )
    publisher_name = SparqlGraphTerm.build_graph_pattern(
        subject=publisher_graph_term,
        predicate=SparqlGraphTerm(namespace_property=foaf.name),
        obj=SparqlGraphTerm(var=name_var),
        close_pattern_with="."
    )
    optional_publisher_same_as = SparqlOptional(
        graphs=[
            SparqlGraphTerm.build_graph_pattern(
                subject=publisher_graph_term,
                predicate=SparqlGraphTerm(namespace_property=owl.sameAs),
                obj=SparqlGraphTerm(var=sameAs),
                close_pattern_with="."
            )
        ]
    )
    where = SparqlWhere(
        graphs=[
            publisher_a_fof_agent,
            publisher_name
        ],
        optional=optional_publisher_same_as
    )

    return SparqlBuilder(
        prefix=prefixes,
        select=select,
        where=where,
        group_by_str=f"{SparqlBuilder.make_var(name_var)} "
                     f"{SparqlBuilder.make_var(publisher)} "
                     f"{SparqlBuilder.make_var(sameAs)} "
    ).build()
