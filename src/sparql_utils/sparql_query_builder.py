from typing import List

from src.sparql_utils.sparql_namespaces import NamespaceProperty, SparqlFunctionString, NoLeafError


class SparqlCount:
    def __init__(self, variable_name: str, as_name: str = None):
        self.variable = variable_name
        self.as_variable = as_name or "count"

    def __str__(self):
        return f"({SparqlFunction.build_string(SparqlFunctionString.COUNT, SparqlBuilder.make_var(self.variable), self.as_variable)})"


class SparqlFunction:
    def __init__(self, fun: SparqlFunctionString, variable: str = None, as_name: str = None, args: List[str] = None,
                 parent=None):
        self.fun = fun
        if variable:
            self.var = variable
        else:
            self.var = False
        if as_name:
            self.as_name = as_name
        else:
            self.as_name = False
        if args:
            self.args = args
        else:
            self.args = False
        self.parent = parent
        self.is_root = parent is None

    def str_with_inner_function(self, inner_fun: str):
        nested_str = f"{self.fun}({inner_fun}"
        if not inner_fun.endswith(")"):
            nested_str += ")"
        if self.as_name:
            nested_str += f" AS ?{self.as_name}"
        return nested_str

    def __str__(self):
        return SparqlFunction.build_string(fun=self.fun, variable=self.var, as_name=self.as_name,
                                           args=self.args)

    @staticmethod
    def build_string(fun: SparqlFunctionString,
                     variable: str,
                     as_name: str = None,
                     args: List[str] = None) -> str:
        fun_str = f"{fun}("
        if variable:
            fun_str += SparqlBuilder.make_var(variable)
        if args:
            fun_str += ")"
            for arg in args:
                fun_str += f", '{arg}'"
        fun_str += ")"
        if as_name:
            fun_str += f" AS ?{as_name}"
        return fun_str

    @staticmethod
    def str_from_hierarchy(leaf_node: 'SparqlFunction') -> str:
        current_node = leaf_node
        func_str = str(leaf_node)
        while True:
            if current_node.is_root:
                break
            else:
                current_node = current_node.parent
                function_node: SparqlFunction = current_node
                func_str = function_node.str_with_inner_function(inner_fun=func_str)
        return func_str


class SparqlGraphTerm:
    def __init__(self, var: str = None, namespace_property: str = None):
        if var:
            self.value = f"?{var}"
        if namespace_property:
            self.value = namespace_property

    @staticmethod
    def build_graph_pattern(subject: 'SparqlGraphTerm',
                            predicate: 'SparqlGraphTerm',
                            obj: 'SparqlGraphTerm',
                            close_pattern_with: str = None) -> str:
        graph_pattern = f"{subject.value} {predicate.value} {obj.value}"
        if close_pattern_with:
            graph_pattern += f" {close_pattern_with}"
        return graph_pattern


class SparqlFilter:
    def __init__(self, filter_string: str = None, filter_on_var: str = None,
                 filter_on_values: List[str] = None) -> object:
        self.filter_string = filter_string
        self.var = filter_on_var
        self.values = filter_on_values

    def __str__(self):
        if self.filter_string:
            return f"FILTER({self.filter_string}) "
        else:
            filter_str_values = ",".join([SparqlFilter.prepare_value(val) for val in self.values])
            return f"FILTER({SparqlBuilder.make_var(self.var)} IN ({filter_str_values}))"

    @staticmethod
    def prepare_value(filter_value: str):
        prepared_value = ""
        if not filter_value.startswith("'"):
            prepared_value = "'"
        prepared_value += filter_value
        if not filter_value.endswith("'"):
            prepared_value += "'"
        return prepared_value

    @staticmethod
    def collect_filters(**filter_params):
        filters = []
        for key, value in filter_params.items():
            if value:
                filters.append(
                    SparqlFilter(filter_on_var=key, filter_on_values=value)
                )
        if len(filters) > 0:
            return filters
        else:
            return None


class SparqlSelect:

    def __init__(self, variable_names: List[str] = None,
                 count_variables: List[SparqlCount] = None,
                 function_variables: List[SparqlFunction] = None):
        self.variable_names = variable_names
        self.count_variables = count_variables
        self.function_variables = function_variables

    def __str__(self):
        return SparqlSelect.select(self.variable_names, self.count_variables, self.function_variables)

    @staticmethod
    def select(variable_names: List[str] = None, count_variables: List[SparqlCount] = None,
               function_variables: List[SparqlFunction] = None) -> str:
        select = "SELECT"
        if not variable_names and not count_variables:
            return f"{select} *"
        else:
            separator: str = " "
            if variable_names:
                sparql_vars = [SparqlBuilder.make_var(x) for x in variable_names]
                select += separator + separator.join(sparql_vars)
            if function_variables:
                functions_strings = [str(x) for x in function_variables]
                select += separator + separator.join(functions_strings)
            if count_variables:
                count_strings = [str(x) for x in count_variables]
                select += separator + separator.join(count_strings)
            return select


class SparqlWhere:
    def __init__(self, graphs: List[str] = None, functions: [SparqlFunction] = None,
                 optional: 'SparqlOptional' = None, nested_clause: str = None, filters: List[SparqlFilter] = None):
        self.graph_patterns = graphs
        self.functions = functions
        self.optional = optional
        self.nested_clause = nested_clause
        self.filters = filters

    def __str__(self) -> str:
        return SparqlWhere.build(graphs=self.graph_patterns,
                                 functions=self.functions,
                                 optional_clause=self.optional,
                                 nested_clause_builder=self.nested_clause,
                                 filters=self.filters)

    @staticmethod
    def build(graphs: List[str] = None,
              functions: [SparqlFunction] = None,
              build_as_optional: bool = False,
              optional_clause: 'SparqlOptional' = None,
              nested_clause_builder: 'SparqlBuilder' = None,
              filters: SparqlFilter = None
              ) -> str:
        if build_as_optional:
            where_str = "OPTIONAL { "
        else:
            where_str = "WHERE { "
        if graphs:
            for pattern in graphs:
                where_str += f"{pattern} "
        if optional_clause:
            where_str += f"{str(optional_clause)} "
        if functions:
            for func in functions:
                if type(func) is str or func.is_root:
                    where_str += f"{str(func)} "
                else:
                    where_str += f"{SparqlFunction.str_from_hierarchy(func)} "
        if nested_clause_builder:
            where_str += "{ "
            where_str += f"{nested_clause_builder.build()} "
            where_str += "} "
        if filters:
            for f in filters:
                where_str += str(f)
        where_str += "} "
        return where_str


class SparqlOptional(SparqlWhere):
    def __init__(self, graphs: List[str] = None, functions: [SparqlFunction] = None, parent: 'SparqlWhere' = None):
        super().__init__(graphs, functions, parent)

    def __str__(self) -> str:
        return SparqlWhere.build(graphs=self.graph_patterns, functions=self.functions, build_as_optional=True)


class SparqlBuilder:

    def __init__(self, prefix: List[NamespaceProperty] = None, select: SparqlSelect = None, where: SparqlWhere = None,
                 group_by_var: str = None, group_by_str: str = None, order_by_str=None):
        self.prefix = prefix
        self.select = select
        self.where = where
        if group_by_var:
            self.group_by = SparqlBuilder.make_var(group_by_var)
        elif group_by_str:
            self.group_by = group_by_str
        else:
            self.group_by = False
        if order_by_str:
            self.order_by = order_by_str
        else:
            self.order_by = False

    @staticmethod
    def make_var(var_str: str) -> str:
        if var_str.startswith("?"):
            return var_str
        else:
            return f"?{var_str}"

    def build(self):
        query_str = ""
        if self.prefix:
            for p in self.prefix:
                query_str += f"{p.get_prefix_definition()} "
        if self.select:
            query_str += f"{str(self.select)} "
        if self.where:
            query_str += f"{str(self.where)}"
        if self.group_by:
            query_str += f"GROUP BY {self.group_by} "
        if self.order_by:
            query_str += f"ORDER BY {self.order_by}"
        return query_str


def encode_for_sparql(string: str):
    return string \
        .replace(" ", "%20") \
        .replace("<", "%3C") \
        .replace(">", "%3E") \
        .replace("(", "%28") \
        .replace(")", "%29") \
        .replace("'", "%27") \
        .replace("*", "%2A").replace("\\", "\\\\")
