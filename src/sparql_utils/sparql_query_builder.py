from typing import List

from src.sparql_utils.sparql_namespaces import NamespaceProperty, SparqlFunctionString, NoLeafError


class SparqlCount:
    def __init__(self, variable_name: str, as_name: str = None):
        self.variable = variable_name
        self.as_variable = as_name or "count"

    def __str__(self):
        return f"({SparqlFunction.build_string(SparqlFunctionString.COUNT, self.variable, self.as_variable)})"


class SparqlFunction:
    def __init__(self, fun: SparqlFunctionString, variable: str = None, as_name: str = None, args: List[str] = None,
                 parent=None):
        self.fun = fun
        if variable:
            self.var = variable
        else:
            self.variable = False
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
        return SparqlFunction.build_string(fun=self.fun, variable=self.var, as_name=self.as_name, args=self.args)

    @staticmethod
    def build_string(fun: SparqlFunctionString,
                     variable: str,
                     as_name: str = None,
                     args: List[str] = None) -> str:
        fun_str = f"{fun}(?{variable}"
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


class SparqlGraphPatternTerm:
    def __init__(self, var: str = None, namespace_property: str = None):
        if var:
            self.value = f"?{var}"
        if namespace_property:
            self.value = namespace_property

    @staticmethod
    def build_graph_pattern(subject: 'SparqlGraphPatternTerm',
                            predicate: 'SparqlGraphPatternTerm',
                            obj: 'SparqlGraphPatternTerm',
                            close_pattern_with: str = None) -> str:
        graph_pattern = f"{subject.value} {predicate.value} {obj.value}"
        if close_pattern_with:
            graph_pattern += f" {close_pattern_with}"
        return graph_pattern


class SparqlSelect:

    def __init__(self, variable_names: List[str] = None, count_variables: List[SparqlCount] = None):
        self.variable_names = variable_names
        self.count_variables = count_variables

    def __str__(self):
        return SparqlSelect.select(self.variable_names, self.count_variables)

    @staticmethod
    def select(variable_names: List[str] = None, count_variables: List[SparqlCount] = None) -> str:
        select = "SELECT"
        if not variable_names and not count_variables:
            return f"{select} *"
        else:
            separator: str = " "
            if variable_names:
                sparql_vars = [SparqlBuilder.__make_var__(x) for x in variable_names]
                select += separator + separator.join(sparql_vars)
            if count_variables:
                count_strings = [str(x) for x in count_variables]
                select += separator + separator.join(count_strings)
            return select


class SparqlWhere:
    def __init__(self, graphs: List[str] = None,
                 functions: [SparqlFunction] = None,
                 parent: 'SparqlWhere' = None):
        self.graph_patterns = graphs
        self.functions = functions
        self.parent = parent
        self.is_root = parent is None

    def __str__(self) -> str:
        if self.is_root:
            return SparqlWhere.build(graphs=self.graph_patterns, functions=self.functions)

    @staticmethod
    def build(graphs: List[str] = None,
              functions: [SparqlFunction] = None) -> str:
        where_str = "WHERE { "
        if graphs:
            for pattern in graphs:
                where_str += f"{pattern} "
        if functions:
            for func in functions:
                if func.is_root:
                    where_str += f"{str(func)} "
                else:
                    where_str += f"{SparqlFunction.str_from_hierarchy(func)} "
        where_str += "} "
        return where_str


class SparqlBuilder:

    def __init__(self, prefix: List[NamespaceProperty], select: SparqlSelect, where: SparqlWhere,
                 group_by_var: str = None, order_by_var: str = None):
        self.prefix = prefix
        self.select = select
        self.where = where
        self.group_by_var = group_by_var
        self.order_by_var = order_by_var

    @staticmethod
    def __make_var__(var_str: str) -> str:
        return f"?{var_str}"


def encode_for_sparql(string: str):
    return string \
        .replace(" ", "%20") \
        .replace("<", "%3C") \
        .replace(">", "%3E") \
        .replace("(", "%28") \
        .replace(")", "%29")
