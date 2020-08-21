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
    type = "a"

    @staticmethod
    def get_prefix_definition() -> str:
        pass


class DCT(NamespaceProperty):
    prefix = "dct:"
    format = f"{prefix}format"
    issued = f"{prefix}issued"
    publisher = f"{prefix}publisher"
    accessRights = f"{prefix}accessRights"
    prefix_definition = "PREFIX dct: <http://purl.org/dc/terms/>"
    provenance = f"{prefix}provenance"
    license = f"{prefix}license"
    source = f"{prefix}source"

    @staticmethod
    def get_prefix_definition() -> str:
        return "PREFIX dct: <http://purl.org/dc/terms/>"

    @staticmethod
    def create_property(from_value: str, **kwargs) -> str:
        return NamespaceProperty.property_string(DCT.prefix, from_value)


class FOAF(NamespaceProperty):
    prefix = "foaf:"
    agent = f"{prefix}Agent"
    name = f"{prefix}name"

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


class DCAT(NamespaceProperty):
    prefix = "dcat:"
    theme = f"{prefix}theme"
    dataset = f"{prefix}Dataset"
    distribution = f"{prefix}distribution"

    @staticmethod
    def get_prefix_definition() -> str:
        return "PREFIX dcat: <http://www.w3.org/ns/dcat%23>"


class XSD(NamespaceProperty):

    @staticmethod
    def get_prefix_definition() -> str:
        return "PREFIX xsd: <http://www.w3.org/2001/XMLSchema%23>"


class SparqlFunctionString:
    DISTINCT = "DISTINCT"
    YEAR = "YEAR"
    MONTH = "MONTH"
    STR = "STR"
    REPLACE = "REPLACE"
    BIND = "BIND"
    LCASE = "LCASE"
    COUNT = "COUNT"
    COALESCE = "COALESCE"

class ContentKeys:
    SRC_ORGANIZATION = "publisher"
    FORMAT = "format"
    WITH_SUBJECT = "withSubject"
    OPEN_DATA = "opendata"
    TOTAL = "total"
    NEW_LAST_WEEK = "new_last_week"
    NATIONAL_COMPONENT = "nationalComponent"
    ORGANIZATION = "organization"
    COUNT = "count"
    VALUE = "value"
    ACCESS_RIGHTS_CODE = "code"
    TIME_SERIES_MONTH = "month"
    TIME_SERIES_YEAR = "year"
    TIME_SERIES_Y_AXIS = "yAxis"
    TIME_SERIES_X_AXIS = "xAxis"
    THEME = "theme"
    ORG_NAME = "name"
    ORGANIZATION_URI = "organization"
