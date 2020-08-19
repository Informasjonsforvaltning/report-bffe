from typing import List

from src.sparql_utils import ContentKeys
from src.sparql_utils.sparql_namespaces import DCT, FOAF, OWL, SparqlFunctionString, RDF, DCAT, XSD
from src.sparql_utils.sparql_query_builder import SparqlSelect, SparqlCount, SparqlWhere, SparqlGraphTerm, \
    SparqlFunction, SparqlBuilder, SparqlOptional, encode_for_sparql, SparqlFilter


def build_datasets_catalog_query(org_uris: List[str], theme: List[str]) -> str:
    prefixes = [DCT, FOAF, OWL]
    select_clause = SparqlSelect(variable_names=[ContentKeys.ORG_NAME, ContentKeys.ORGANIZATION_URI],
                                 count_variables=[SparqlCount(variable_name="item", as_name="count")]
                                 )
    where_clause = catalog_query_where_clause(org_uris, theme)

    query = SparqlBuilder(
        prefix=prefixes,
        select=select_clause,
        where=where_clause,
        group_by_str=f"?{ContentKeys.ORGANIZATION_URI} ?{ContentKeys.ORG_NAME}"
    ).build()
    return encode_for_sparql(query)


def catalog_query_where_clause(org_uris: List[str], theme: List[str]):
    bind_root = SparqlFunction(fun=SparqlFunctionString.BIND).str_with_inner_function("COALESCE(?sameAs, STR("
                                                                                      "?publisher)) AS ?organization")
    publisher_var = "publisher"
    publisher_a_foaf_a_agent = SparqlGraphTerm.build_graph_pattern(
        subject=SparqlGraphTerm(var="publisher"),
        predicate=SparqlGraphTerm(namespace_property=RDF.type),
        obj=SparqlGraphTerm(namespace_property=FOAF.agent),
        close_pattern_with="."
    )
    publisher_name_pattern = SparqlGraphTerm.build_graph_pattern(
        subject=SparqlGraphTerm(var=publisher_var),
        predicate=SparqlGraphTerm(namespace_property=FOAF.name),
        obj=SparqlGraphTerm(var=ContentKeys.ORG_NAME),
        close_pattern_with="."
    )

    graph_patterns = [
        publisher_a_foaf_a_agent,
        SparqlGraphTerm.build_graph_pattern(
            subject=SparqlGraphTerm(var="item"),
            predicate=SparqlGraphTerm(namespace_property=DCT.publisher),
            obj=SparqlGraphTerm(var=publisher_var),
            close_pattern_with="."
        ),
        publisher_name_pattern
    ]
    nested_select_clause = SparqlSelect(variable_names=["publisher", "organization"])
    nested_where = SparqlWhere(graphs=[publisher_a_foaf_a_agent],
                               functions=[bind_root],
                               optional=SparqlOptional(graphs=[
                                   SparqlGraphTerm.build_graph_pattern(
                                       subject=SparqlGraphTerm(var="publisher"),
                                       predicate=SparqlGraphTerm(namespace_property=OWL.sameAs),
                                       obj=SparqlGraphTerm(var="sameAs"),
                                       close_pattern_with="."
                                   )
                               ]),
                               filters=SparqlFilter.collect_filters(organization=org_uris)
                               )
    nested_builder = SparqlBuilder(select=nested_select_clause, where=nested_where)
    return SparqlWhere(graphs=graph_patterns, nested_clause=nested_builder)


def build_datasets_access_rights_query(org_uris: List[str], theme) -> str:
    code_var = ContentKeys.ACCESS_RIGHTS_CODE
    prefixes = [DCT]
    select = SparqlSelect(variable_names=[code_var], count_variables=[SparqlCount(variable_name=code_var)])
    where_filters = SparqlFilter.collect_filters(organization=org_uris)
    var_dataset = "dataset"
    var_publisher = "publisher"
    var_organization = "organization"
    where_graphs = [
        SparqlGraphTerm.build_graph_pattern(
            subject=SparqlGraphTerm(var=var_dataset),
            predicate=SparqlGraphTerm(namespace_property=DCT.accessRights),
            obj=SparqlGraphTerm(var=code_var),
            close_pattern_with="."
        ),
    ]
    where_functions = None
    if where_filters:
        where_graphs.append(
            SparqlGraphTerm.build_graph_pattern(
                SparqlGraphTerm(var=var_dataset),
                SparqlGraphTerm(namespace_property=DCT.publisher),
                SparqlGraphTerm(var=var_publisher),
                close_pattern_with="."
            )
        )
        where_functions = [
            SparqlFunction(fun=SparqlFunctionString.STR, variable=var_publisher, as_name=var_organization,
                           parent=SparqlFunction(SparqlFunctionString.BIND))
        ]

    query = SparqlBuilder(
        prefix=prefixes,
        select=select,
        where=SparqlWhere(graphs=where_graphs,
                          functions=where_functions,
                          filters=where_filters
                          ),
        group_by_var=code_var
    ).build()
    return encode_for_sparql(query)


def build_datasets_formats_query(org_uris: List[str], theme) -> str:
    prefixes = [DCT]
    if org_uris:
        prefixes.append(DCAT)
    select = SparqlSelect(
        variable_names=[ContentKeys.FORMAT],
        count_variables=[(SparqlCount(variable_name=ContentKeys.FORMAT))]
    )
    var_distribution = "distribution"
    var_publisher = "publisher"
    var_org = "org"
    fun_bind = SparqlFunction(fun=SparqlFunctionString.BIND)
    fun_lcase_leaf = SparqlFunction(fun=SparqlFunctionString.LCASE, variable="distributionFormat", as_name="format",
                                    parent=fun_bind)
    fun_org_str_leaf = SparqlFunction(fun=SparqlFunctionString.STR, variable=var_publisher, as_name=var_org,
                                      parent=fun_bind)
    where_graphs = []
    if org_uris:
        where_graphs.append(
            SparqlGraphTerm.build_graph_pattern(
                SparqlGraphTerm(var="dataset"),
                SparqlGraphTerm(namespace_property=DCAT.distribution),
                SparqlGraphTerm(var=var_distribution),
                close_pattern_with="."
            )
        )
        where_graphs.append(
            SparqlGraphTerm.build_graph_pattern(
                SparqlGraphTerm(var="dataset"),
                SparqlGraphTerm(namespace_property=DCT.publisher),
                SparqlGraphTerm(var=var_publisher),
                close_pattern_with="."
            )
        )

    where_graphs.append(
        SparqlGraphTerm.build_graph_pattern(
            subject=SparqlGraphTerm(var=var_distribution),
            predicate=SparqlGraphTerm(namespace_property=DCT.format),
            obj=SparqlGraphTerm(var="distributionFormat"),
            close_pattern_with="."
        )
    )

    where_functions = [fun_lcase_leaf]
    if org_uris:
        where_functions.append(fun_org_str_leaf)
    where = SparqlWhere(graphs=where_graphs, functions=where_functions,
                        filters=SparqlFilter.collect_filters(org=org_uris))
    query = SparqlBuilder(prefix=prefixes, select=select, where=where, group_by_var="format").build()
    return encode_for_sparql(query)


def build_datasets_themes_query(org_uris: List[str], theme) -> str:
    prefixes = [DCAT]
    if org_uris:
        prefixes.append(DCT)
    select = SparqlSelect(
        variable_names=[ContentKeys.THEME],
        count_variables=[SparqlCount(variable_name=ContentKeys.THEME)]
    )
    var_dataset = "dataset"
    var_org = "org"
    var_publisher = "publisher"
    where_graphs = [
        SparqlGraphTerm.build_graph_pattern(
            subject=SparqlGraphTerm(var=var_dataset),
            predicate=SparqlGraphTerm(namespace_property=DCAT.theme),
            obj=SparqlGraphTerm(var=ContentKeys.THEME),
            close_pattern_with="."
        )
    ]

    if org_uris:
        where_graphs.append(
            SparqlGraphTerm.build_graph_pattern(
                subject=SparqlGraphTerm(var=var_dataset),
                predicate=SparqlGraphTerm(namespace_property=DCT.publisher),
                obj=SparqlGraphTerm(var=var_publisher)
            )
        )

    where_functions = None
    if org_uris:
        where_functions = [
            SparqlFunction(fun=SparqlFunctionString.STR, variable=var_publisher, as_name=var_org,
                           parent=SparqlFunction(fun=SparqlFunctionString.BIND))
        ]
    where = SparqlWhere(graphs=where_graphs,
                        filters=SparqlFilter.collect_filters(org=org_uris),
                        functions=where_functions)

    query = SparqlBuilder(prefix=prefixes, select=select, where=where, group_by_var=ContentKeys.THEME).build()
    return encode_for_sparql(query)


def build_dataset_time_series_query():
    base_var = "d"
    issued_var = "issued"
    prefixes = [DCT]
    select = SparqlSelect(
        variable_names=[ContentKeys.TIME_SERIES_MONTH, ContentKeys.TIME_SERIES_YEAR],
        count_variables=[SparqlCount(variable_name=base_var, as_name=ContentKeys.COUNT)]
    )
    where = SparqlWhere(graphs=[
        SparqlGraphTerm.build_graph_pattern(
            subject=SparqlGraphTerm(var=base_var),
            predicate=SparqlGraphTerm(namespace_property=DCT.issued),
            obj=SparqlGraphTerm(var=issued_var),
            close_pattern_with="."
        )
    ])

    month_fun = SparqlFunction(SparqlFunctionString.MONTH, variable=issued_var, as_name=ContentKeys.TIME_SERIES_MONTH)
    year_fun = SparqlFunction(SparqlFunctionString.YEAR, variable=issued_var, as_name=ContentKeys.TIME_SERIES_YEAR)
    group_by_str = f"({str(month_fun)}) ({str(year_fun)})"
    order_by = f"ASC(?{ContentKeys.TIME_SERIES_YEAR}) ASC(?{ContentKeys.TIME_SERIES_MONTH})"
    query = SparqlBuilder(prefix=prefixes,
                          select=select,
                          where=where,
                          group_by_str=group_by_str,
                          order_by_str=order_by).build()
    return encode_for_sparql(query)


def build_dataset_simple_statistic_query(field: ContentKeys, org_uris: [List[str]], theme):
    return simple_stat_functions[field](org_uris=org_uris, theme=theme)


def build_datasets_total_query(org_uris: [List[str]], theme):
    prefix = [DCAT, DCT]
    dataset_var = "dataaset"
    publisher_var = "publisher"
    publisher_str_var = "org"
    where_graphs = [
        SparqlGraphTerm.build_graph_pattern(
            subject=SparqlGraphTerm(var=dataset_var),
            predicate=SparqlGraphTerm(namespace_property=RDF.type),
            obj=SparqlGraphTerm(namespace_property=DCAT.dataset),
            close_pattern_with="."
        )
    ]
    functions = []
    if org_uris:
        where_graphs.append(build_dataset_publisher_graph(dataset_var=dataset_var, publisher_var=publisher_var))
        functions.append(build_publisher_str_function(publisher_var=publisher_var, publisher_str_var=publisher_str_var))

    select = SparqlSelect(count_variables=[SparqlCount(variable_name=dataset_var, as_name=ContentKeys.TOTAL)])
    where = SparqlWhere(graphs=where_graphs, functions=functions, filters=SparqlFilter.collect_filters(org=org_uris))
    query = SparqlBuilder(prefix=prefix, select=select, where=where).build()
    return encode_for_sparql(query)


def build_datasets_with_subject_query(org_uris: List[str], theme):
    prefix = [DCAT, DCT]
    dataset_var = "dataset"
    publisher_var = "publisher"
    publisher_str_var = "org"
    where_graphs = [
        SparqlGraphTerm.build_graph_pattern(
            subject=SparqlGraphTerm(var=dataset_var),
            predicate=SparqlGraphTerm(namespace_property=RDF.type),
            obj=SparqlGraphTerm(namespace_property=DCAT.dataset),
            close_pattern_with="."
        )
    ]
    filters = [SparqlFilter(filter_string="EXISTS {?dataset dct:subject ?subject .}")]
    functions = []
    if org_uris:
        where_graphs.append(build_dataset_publisher_graph(dataset_var=dataset_var, publisher_var=publisher_var))
        functions.append(build_publisher_str_function(publisher_var=publisher_var, publisher_str_var=publisher_str_var))
        org_filter = SparqlFilter(filter_on_var=publisher_str_var, filter_on_values=org_uris)
        filters.append(org_filter)

    select = SparqlSelect(count_variables=[SparqlCount(variable_name=dataset_var, as_name=ContentKeys.WITH_SUBJECT)])
    where = SparqlWhere(graphs=where_graphs, functions=functions, filters=filters)
    query = SparqlBuilder(prefix=prefix, select=select, where=where).build()
    return encode_for_sparql(query)


def build_dataset_open_data_query(org_uris: List[str], theme):
    # TODO: get reference data from
    # https://fellesdatakatalog.digdir.no/reference-data/codes/openlicenses
    # get public accessright from referenced data store

    open_licenses = ['http://data.norge.no/nlod/',
                     'http://data.norge.no/nlod/no/1.0',
                     'http://data.norge.no/nlod/no/2.0',
                     'http://creativecommons.org/licenses/by/4.0/',
                     'http://creativecommons.org/licenses/by/4.0/deed.no',
                     'http://creativecommons.org/publicdomain/zero/1.0/']

    public_access_right = '<http://publications.europa.eu/resource/authority/access-right/PUBLIC>'

    d_var = "d"
    access_right_var = "accessRights"
    dist_var = "distribution"
    dct_license_var = "l"
    license_source_var = "src"
    all_licenses_var = "license"
    publisher_var = "publisher"
    publisher_str_var= "org"
    prefix = [DCAT, DCT]
    select = SparqlSelect(
        count_variables=[SparqlCount(variable_name=d_var, as_name=ContentKeys.OPEN_DATA,
                                     inner_function=SparqlFunctionString.DISTINCT)]
    )
    where_graphs = [
        build_var_a_dataset_graph(d_var),
        SparqlGraphTerm.build_graph_pattern(
            SparqlGraphTerm(var=d_var),
            SparqlGraphTerm(namespace_property=DCT.accessRights),
            SparqlGraphTerm(var=access_right_var),
            close_pattern_with="."
        ),
        SparqlGraphTerm.build_graph_pattern(
            SparqlGraphTerm(var=d_var),
            SparqlGraphTerm(namespace_property=DCAT.distribution),
            SparqlGraphTerm(var=dist_var),
            "."
        ),
        SparqlGraphTerm.build_graph_pattern(
            SparqlGraphTerm(var=dist_var),
            SparqlGraphTerm(namespace_property=DCT.license),
            SparqlGraphTerm(var=dct_license_var),
            "."
        )
    ]

    optional = SparqlOptional(
        graphs=[
            SparqlGraphTerm.build_graph_pattern(
                SparqlGraphTerm(var=dct_license_var),
                SparqlGraphTerm(namespace_property=DCT.source),
                SparqlGraphTerm(var=license_source_var),
                "."
            )

        ]
    )
    combine_licenses_function = SparqlFunction(
        fun=SparqlFunctionString.BIND).str_with_inner_function(
        f"COALESCE(?{license_source_var}, STR(?{dct_license_var})) AS ?{all_licenses_var}")
    functions = [combine_licenses_function]
    filters = SparqlFilter.collect_filters(license=open_licenses)
    filters.append(
        SparqlFilter(filter_string=f"?{access_right_var}={public_access_right}")
    )

    if org_uris:
        where_graphs.append(build_dataset_publisher_graph(dataset_var=d_var, publisher_var=publisher_var))
        functions.append(build_publisher_str_function(publisher_var=publisher_var, publisher_str_var=publisher_str_var))
        org_filter = SparqlFilter(filter_on_var=publisher_str_var, filter_on_values=org_uris)
        filters.append(org_filter)

    where = SparqlWhere(
        graphs=where_graphs,
        functions=functions,
        optional=optional,
        filters=filters
    )

    query = SparqlBuilder(
        prefix=prefix,
        select=select,
        where=where
    ).build()
    return encode_for_sparql(query)


def build_datasets_new_last_week_query(org_uris: List[str], theme) -> str:
    prefix = [DCT, XSD]
    d_var = "d"
    issued_var = "issued"
    select = SparqlSelect(count_variables=[SparqlCount(variable_name=d_var, as_name=ContentKeys.NEW_LAST_WEEK)])
    where_graphs = [
        SparqlGraphTerm.build_graph_pattern(
            SparqlGraphTerm(var=d_var),
            SparqlGraphTerm(namespace_property=DCT.issued),
            SparqlGraphTerm(var=issued_var)
        )
    ]
    filters = [SparqlFilter(filter_string='?issued >= (NOW() - "P7D"^^xsd:duration ) ')]
    where = SparqlWhere(
        graphs=where_graphs,
        filters=filters
    )

    query = SparqlBuilder(
        prefix=prefix,
        select=select,
        where=where
    ).build()
    return encode_for_sparql(query)


def build_datasets_national_component_query(org_uris: List[str], theme) -> str:
    d_var = "d"
    provenance_var = "provenance"
    national_provenance_uri = "<http://data.brreg.no/datakatalog/provinens/nasjonal>"
    prefix = [DCT, DCAT]
    select = SparqlSelect(count_variables=[SparqlCount(variable_name=d_var, as_name=ContentKeys.NATIONAL_COMPONENT)])
    a_dataset_pattern = build_var_a_dataset_graph(d_var)
    where_graphs = [
        a_dataset_pattern,
        SparqlGraphTerm.build_graph_pattern(
            SparqlGraphTerm(var=d_var),
            SparqlGraphTerm(namespace_property=DCT.provenance),
            SparqlGraphTerm(var=provenance_var)
        )
    ]

    filters = [
        SparqlFilter(filter_string=f"?{provenance_var}={national_provenance_uri}")
    ]

    where = SparqlWhere(
        graphs=where_graphs,
        filters=filters
    )

    query = SparqlBuilder(
        prefix=prefix,
        select=select,
        where=where
    ).build()
    return encode_for_sparql(query)


simple_stat_functions = {
    ContentKeys.TOTAL: build_datasets_total_query,
    ContentKeys.OPEN_DATA: build_dataset_open_data_query,
    ContentKeys.NATIONAL_COMPONENT: build_datasets_national_component_query,
    ContentKeys.WITH_SUBJECT: build_datasets_with_subject_query,
    ContentKeys.NEW_LAST_WEEK: build_datasets_new_last_week_query
}


def build_var_a_dataset_graph(var: str):
    return SparqlGraphTerm.build_graph_pattern(
        subject=SparqlGraphTerm(var=var),
        predicate=SparqlGraphTerm(namespace_property=RDF.type),
        obj=SparqlGraphTerm(namespace_property=DCAT.dataset),
        close_pattern_with="."
    )


def build_publisher_str_function(publisher_var: str, publisher_str_var: str):
    fun_bind = SparqlFunction(fun=SparqlFunctionString.BIND)
    return SparqlFunction(fun=SparqlFunctionString.STR, variable=publisher_var, as_name=publisher_str_var,
                          parent=fun_bind)


def build_dataset_publisher_graph(dataset_var: str, publisher_var):
    return SparqlGraphTerm.build_graph_pattern(
        SparqlGraphTerm(var=dataset_var),
        SparqlGraphTerm(namespace_property=DCT.publisher),
        SparqlGraphTerm(var=publisher_var),
        close_pattern_with="."
    )
