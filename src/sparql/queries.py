from src.rdf_namespaces import DCAT, DCT, FOAF, OWL, RDF, NamespaceProperty
from src.sparql.builder import (
    FromGraph,
    SparqlBuilder,
    SparqlGraphTerm,
    SparqlOptional,
    SparqlSelect,
    SparqlWhere,
)
from src.utils import ContentKeys


def build_dataset_publisher_query():
    dct = DCT(NamespaceProperty.TTL)
    foaf = FOAF(NamespaceProperty.TTL)
    owl = OWL(NamespaceProperty.TTL)
    rdf = RDF(NamespaceProperty.TTL)
    prefixes = [dct, foaf, owl]
    name_var = ContentKeys.ORG_NAME
    publisher = ContentKeys.PUBLISHER
    publisher_graph_term = SparqlGraphTerm(var=publisher)
    same_as = ContentKeys.SAME_AS
    select = SparqlSelect(
        variable_names=[name_var, publisher, same_as], from_graph=FromGraph.DATASETS
    )
    publisher_a_fof_agent = SparqlGraphTerm.build_graph_pattern(
        subject=publisher_graph_term,
        predicate=SparqlGraphTerm(namespace_property=rdf.type),
        obj=SparqlGraphTerm(namespace_property=foaf.agent),
        close_pattern_with=".",
    )
    publisher_name = SparqlGraphTerm.build_graph_pattern(
        subject=publisher_graph_term,
        predicate=SparqlGraphTerm(namespace_property=foaf.name),
        obj=SparqlGraphTerm(var=name_var),
        close_pattern_with=".",
    )
    optional_publisher_same_as = SparqlOptional(
        graphs=[
            SparqlGraphTerm.build_graph_pattern(
                subject=publisher_graph_term,
                predicate=SparqlGraphTerm(namespace_property=owl.sameAs),
                obj=SparqlGraphTerm(var=same_as),
                close_pattern_with=".",
            )
        ]
    )
    where = SparqlWhere(
        graphs=[publisher_a_fof_agent, publisher_name],
        optional=optional_publisher_same_as,
    )

    return SparqlBuilder(
        prefix=prefixes,
        select=select,
        where=where,
        group_by_str=f"{SparqlBuilder.make_var(name_var)} "
        f"{SparqlBuilder.make_var(publisher)} "
        f"{SparqlBuilder.make_var(same_as)} ",
    ).build()


def build_dataservice_query():
    dct = DCT(NamespaceProperty.TTL)
    dcat = DCAT(NamespaceProperty.TTL)
    foaf = FOAF(NamespaceProperty.TTL)
    owl = OWL(NamespaceProperty.TTL)
    rdf = RDF(NamespaceProperty.TTL)
    prefixes = [dct, dcat, foaf, owl]
    title = ContentKeys.TITLE
    issued = ContentKeys.ISSUED
    catalog_graph_term = SparqlGraphTerm(var="catalog")
    record_graph_term = SparqlGraphTerm(var="record")
    select = SparqlSelect(
        variable_names=[title, issued, "sameAs", ContentKeys.MEDIATYPE],
        from_graph=FromGraph.DATASERVICE,
    )

    catalog_a_dcat_catalog = SparqlGraphTerm.build_graph_pattern(
        subject=catalog_graph_term,
        predicate=SparqlGraphTerm(namespace_property=rdf.type),
        obj=SparqlGraphTerm(namespace_property=dcat.type_catalog),
        close_pattern_with=".",
    )

    catalog_dct_publisher = SparqlGraphTerm.build_graph_pattern(
        subject=catalog_graph_term,
        predicate=SparqlGraphTerm(namespace_property=dct.publisher),
        obj=SparqlGraphTerm(var=ContentKeys.PUBLISHER),
        close_pattern_with=".",
    )

    catalog_dcat_service = SparqlGraphTerm.build_graph_pattern(
        subject=catalog_graph_term,
        predicate=SparqlGraphTerm(namespace_property=dcat.type_service),
        obj=SparqlGraphTerm(var=ContentKeys.SERVICE),
        close_pattern_with=".",
    )

    record_foaf_primary_topic_service = SparqlGraphTerm.build_graph_pattern(
        subject=record_graph_term,
        predicate=SparqlGraphTerm(namespace_property=foaf.primaryTopic),
        obj=SparqlGraphTerm(var=ContentKeys.SERVICE),
        close_pattern_with=".",
    )

    service_dct_title = SparqlGraphTerm.build_graph_pattern(
        subject=SparqlGraphTerm(var=ContentKeys.SERVICE),
        predicate=SparqlGraphTerm(namespace_property=dct.title),
        obj=SparqlGraphTerm(var=ContentKeys.TITLE),
        close_pattern_with=".",
    )

    record_dct_issued = SparqlGraphTerm.build_graph_pattern(
        subject=SparqlGraphTerm(var="record"),
        predicate=SparqlGraphTerm(namespace_property=dct.issued),
        obj=SparqlGraphTerm(var=ContentKeys.ISSUED),
        close_pattern_with=".",
    )

    publisher_owl_same_as = SparqlGraphTerm.build_graph_pattern(
        subject=SparqlGraphTerm(var=ContentKeys.PUBLISHER),
        predicate=SparqlGraphTerm(namespace_property=owl.sameAs),
        obj=SparqlGraphTerm(var=ContentKeys.SAME_AS),
        close_pattern_with=".",
    )

    service_dcat_mediatype = SparqlGraphTerm.build_graph_pattern(
        subject=SparqlGraphTerm(var=ContentKeys.SERVICE),
        predicate=SparqlGraphTerm(namespace_property=dcat.mediaType),
        obj=SparqlGraphTerm(var=ContentKeys.MEDIATYPE),
        close_pattern_with=".",
    )

    where = SparqlWhere(
        graphs=[
            catalog_a_dcat_catalog,
            catalog_dct_publisher,
            catalog_dcat_service,
            record_foaf_primary_topic_service,
            service_dct_title,
            record_dct_issued,
            publisher_owl_same_as,
            service_dcat_mediatype,
        ]
    )

    return SparqlBuilder(prefix=prefixes, select=select, where=where).build()


def build_dataservice_publisher_query():
    dct = DCT(NamespaceProperty.TTL)
    dcat = DCAT(NamespaceProperty.TTL)
    foaf = FOAF(NamespaceProperty.TTL)
    owl = OWL(NamespaceProperty.TTL)
    rdf = RDF(NamespaceProperty.TTL)
    prefixes = [dct, dcat, foaf, owl]
    publisher = ContentKeys.PUBLISHER
    publisher_graph_term = SparqlGraphTerm(var=publisher)
    same_as = ContentKeys.SAME_AS
    select = SparqlSelect(
        variable_names=[publisher, same_as], from_graph=FromGraph.DATASERVICE
    )
    publisher_a_fof_agent = SparqlGraphTerm.build_graph_pattern(
        subject=publisher_graph_term,
        predicate=SparqlGraphTerm(namespace_property=rdf.type),
        obj=SparqlGraphTerm(namespace_property=foaf.agent),
        close_pattern_with=".",
    )
    optional_publisher_same_as = SparqlOptional(
        graphs=[
            SparqlGraphTerm.build_graph_pattern(
                subject=publisher_graph_term,
                predicate=SparqlGraphTerm(namespace_property=owl.sameAs),
                obj=SparqlGraphTerm(var=same_as),
                close_pattern_with=".",
            )
        ]
    )
    where = SparqlWhere(
        graphs=[publisher_a_fof_agent], optional=optional_publisher_same_as
    )

    return SparqlBuilder(
        prefix=prefixes,
        select=select,
        where=where,
        group_by_str=f"{SparqlBuilder.make_var(publisher)} "
        f"{SparqlBuilder.make_var(same_as)} ",
    ).build()
