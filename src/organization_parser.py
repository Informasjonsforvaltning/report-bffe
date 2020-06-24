import re

NATIONAL_REGISTRY_PATTERN = "data.brreg.no/enhetsregisteret"


class ParsedOrganization:

    def __init__(self, name, orgPath=None, org_id=None, uri=None):
        self.name = name
        self.org_id = ParsedOrganization.resolve_id(org_id, uri)
        self.orgPath = self.resolve_org_path(orgPath)

    def __eq__(self, other):
        """
        Performs a best attempt for matching organizations:
            comparator or name as fallback
        :param other:
        :return:
        """
        if isinstance(other, str):
            if other == self.get_comparator():
                return True
            else:
                return other == self.name
        elif isinstance(other, ParsedOrganization):
            if other.get_comparator() == self.get_comparator():
                return True
            else:
                return other.name == self.name
        elif isinstance(other, list):
            return self.__eq_on_org_path(other)
        else:
            return False

    def __eq_on_org_path(self, other_org_path: list):
        self_org_path_list = self.orgPath.split("/")
        if self_org_path_list.__len__() < other_org_path.__len__():
            return False
        for i in range(0, len(other_org_path)):
            if other_org_path[i] != self_org_path_list[i]:
                return False
        return True

    def get_comparator(self):
        try:
            if self.org_id:
                return self.org_id
            else:
                return self.name
        except AttributeError:
            return self.name

    def resolve_org_path(self, org_path:str):
        if org_path:
            if org_path.startswith("/"):
                return org_path[1:org_path.__len__()-1]
            else:
                return org_path
        return f"ANNET/{self.name}"

    @staticmethod
    def is_national_registry_uri(uri: str) -> bool:
        return re.findall(NATIONAL_REGISTRY_PATTERN, uri).__len__() > 0

    @staticmethod
    def resolve_id(org_id=None, uri=None):
        if org_id:
            return org_id
        elif uri and ParsedOrganization.is_national_registry_uri(uri):
            uri_components = uri.split("/")
            return uri_components[len(uri_components) - 1]
        else:
            return None

    @staticmethod
    def from_organizations_catalog_json(json: dict):
        return ParsedOrganization(name=json["name"],
                                  orgPath=json["orgPath"],
                                  uri=json["norwegianRegistry"],
                                  org_id=json["organizationId"])

    @staticmethod
    def from_harvester_elastic_result(param):
        pass
