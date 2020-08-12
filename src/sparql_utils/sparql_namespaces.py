import abc


class NamespaceProperty(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def get_prefix_definition():
        pass

    @staticmethod
    def property_string(prefix: str, from_value: str) -> str:
        return f"{prefix}{from_value}"


class RDF(NamespaceProperty):
    prefix = "rdf: "
    TYPE = "a"

    @staticmethod
    def get_prefix_definition() -> str:
        pass


class DCT(NamespaceProperty):
    prefix = "dct:"
    format = f"{prefix}format"
    publisher = f"{prefix}publisher"
    prefix_definition = "PREFIX dct: <http://purl.org/dc/terms/>"

    @staticmethod
    def get_prefix_definition() -> str:
        return "PREFIX dct: <http://purl.org/dc/terms/>"

    @staticmethod
    def create_property(from_value: str, **kwargs) -> str:
        return NamespaceProperty.property_string(DCT.prefix, from_value)


class FOAF(NamespaceProperty):
    prefix = "foaf:"
    agent = f"{prefix}Agent"

    @staticmethod
    def get_prefix_definition() -> str:
        return "PREFIX foaf: <http://xmlns.com/foaf/0.1/>"

    @staticmethod
    def create_property(from_value: str, **kwargs) -> str:
        return NamespaceProperty.property_string(FOAF.prefix, from_value)


class OWL(NamespaceProperty):
    prefix = "owl:"
    agent = f"{prefix}Agent"
    sameAs = f"{prefix}sameAs"

    @staticmethod
    def get_prefix_definition() -> str:
        return "PREFIX owl: <http://www.w3.org/2002/07/owl%23>"

    @staticmethod
    def create_property(from_value: str, **kwargs) -> str:
        return NamespaceProperty.property_string(FOAF.prefix, from_value)


class SparqlFunctionString:
    STR = "STR"
    REPLACE = "REPLACE"
    BIND = "BIND"
    LCASE = "LCASE"
    COUNT = "COUNT"
    COALESCE = "COALESCE"


class NoLeafError(Exception):
    def __init__(self, node_list):
        self.message = f"No leaf node found in {node_list}"
