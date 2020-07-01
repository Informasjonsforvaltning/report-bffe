class NotAServiceKeyException(Exception):
    def __init__(self, string_key: str):
        self.reason = f"service not recognized: {string_key}"


class ServiceKey:
    ORGANIZATIONS = "organizations"
    INFO_MODELS = "informationmodels"
    DATA_SERVICES = "dataservices"
    DATA_SETS = "datasets"
    CONCEPTS = "concepts"

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
