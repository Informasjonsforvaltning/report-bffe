class ServiceKey:
    ORGANIZATIONS = "organizations"
    INFO_MODELS = "informationmodels"
    DATA_SERVICES = "dataservices"
    DATA_SETS = "datasets"
    CONCEPTS = "concepts"
    REFERENCE_DATA = "reference_data"

    @staticmethod
    def get_key(string_key: str) -> 'ServiceKey':
        if string_key == ServiceKey.ORGANIZATIONS:
            return ServiceKey.ORGANIZATIONS
        if string_key == ServiceKey.INFO_MODELS:
            return ServiceKey.INFO_MODELS
        if string_key == ServiceKey.DATA_SERVICES:
            return ServiceKey.DATA_SERVICES
        if string_key == ServiceKey.DATA_SETS:
            return ServiceKey.DATA_SETS
        if string_key == ServiceKey.CONCEPTS:
            return ServiceKey.CONCEPTS
        else:
            raise NotAServiceKeyException(string_key)


class QueryParameter:
    ORG_PATH = "orgPath"
    THEME = "theme"


class NotAServiceKeyException(Exception):
    def __init__(self, string_key: str):
        self.status = 400
        self.reason = f"service not recognized: {string_key}"


class FetchFromServiceException(Exception):
    def __init__(self, execution_point: str, url: str = None):
        self.status = 500
        self.reason = f"Connection error when attempting to fetch {execution_point} from {url}"


class NotInNationalRegistryException(Exception):
    def __init__(self, uri):
        self.reason = f"{uri} was not found in the nationalRegistry"


class BadOrgPathException(Exception):
    def __init__(self, org_path):
        self.reason = f"could not find any organization with {org_path}"