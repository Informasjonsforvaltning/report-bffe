import re
from typing import List

from src.utils import BadOrgPathException, NoOrganizationEntriesException

NATIONAL_REGISTRY_PATTERN = "data.brreg.no/enhetsregisteret"


class ParsedOrganization:

    def __init__(self, name, orgPath=None, org_id=None, uri=None):
        self.name = name
        self.org_id = ParsedOrganization.resolve_id(org_id, uri)
        self.orgPath = self.resolve_org_path(orgPath)
        self.uri = uri
        self.dataset_reference_uri = None

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
            elif ParsedOrganization.is_national_registry_uri(other):
                return ParsedOrganization.resolve_id(uri=other) == self.get_comparator()
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

    def resolve_org_path(self, org_path: str):
        if org_path:
            return org_path
        return f"/ANNET/{self.name}"

    def has_national_registry_entry(self):
        return not self.orgPath.startswith("/ANNET")

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

    @staticmethod
    def parse_list(org_list: list):
        parsed_list = []
        for org in org_list:
            parsed_list.append(ParsedOrganization.from_organizations_catalog_json(org))
        return parsed_list


class OrganizationStore:
    __instance__: 'OrganizationStore' = None

    def __init__(self):
        if OrganizationStore.__instance__ is None:
            self.organizations: List = None
            self.modified = False
            OrganizationStore.__instance__ = self
        else:
            raise OrganizationStoreExistsException()

    def update(self, organizations: List[ParsedOrganization] = None):
        if not self.organizations:
            self.organizations = organizations

    def add_organization(self, organization: ParsedOrganization):
        if organization not in self.organizations:
            self.organizations.append(organization)
            self.modified = True

    def get_dataset_reference_for_orgpath(self, orgpath: str) -> List[str]:
        try:
            org_uris = [org.dataset_reference_uri for org in self.organizations if
                        org == orgpath.split("/") and org.dataset_reference_uri is not None]
        except TypeError:
            raise NoOrganizationEntriesException()

        if len(org_uris) == 0:
            raise BadOrgPathException(org_path=orgpath)
        else:
             return org_uris

    @staticmethod
    def get_instance():
        if OrganizationStore.__instance__:
            return OrganizationStore.__instance__
        else:
            return OrganizationStore()


class OrganizationStoreExistsException(Exception):
    def __init__(self):
        self.message = "organization store is already created"
