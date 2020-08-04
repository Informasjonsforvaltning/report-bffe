import abc


class NamespaceProperty:
    RDF_TYPE = "a"

    @staticmethod
    def property_string(prefix: str, from_value: str) -> str:
        return f"{prefix}{from_value}"


class DCT(NamespaceProperty):
    prefix = "dct:"
    format = f"{prefix}format"
    prefix_definition = "PREFIX dct: <http://purl.org/dc/terms/>"

    @staticmethod
    def create_property(from_value: str, **kwargs) -> str:
        return NamespaceProperty.property_string(DCT.prefix, from_value)


class FOAF(NamespaceProperty):
    prefix = "foaf:"
    agent = f"{prefix}Agent"

    @staticmethod
    def create_property(from_value: str, **kwargs) -> str:
        return NamespaceProperty.property_string(FOAF.prefix, from_value)


class SparqlFunctionString:
    STR = "STR"
    REPLACE = "REPLACE"
    BIND = "BIND"
    LCASE = "LCASE"
    COUNT = "COUNT"


class NoLeafError(Exception):
    def __init__(self, node_list):
        self.message = f"No leaf node found in {node_list}"
