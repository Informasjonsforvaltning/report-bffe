from typing import List

from src.utils import NATIONAL_REGISTRY_PATTERN, ContentKeys, OrgCatalogKeys


class OrganizationReferencesObject:
    def __init__(
        self,
        org_uri: str = None,
        org_path: str = None,
        same_as_entry: str = None,
        name: str = None,
    ):
        self.org_uri: str = org_uri
        self.org_path: str = org_path
        self.same_as: List[str] = list()
        if same_as_entry:
            self.same_as.append(same_as_entry)
        self.name: str = name

    def __eq__(self, other):
        if type(other) == OrganizationReferencesObject:
            if self.org_uri:
                if self.__eq_on_org_uri(other):
                    return True
                else:
                    return self.__eq_on_same_as(other)
            elif self.same_as and other.same_as:
                return self.__eq_on_same_as(other)
        elif type(other) == str:
            if not self.org_path:
                return False
            else:
                return self.org_path == other
        else:
            return False

    def __eq_on_org_uri(self, other: "OrganizationReferencesObject"):
        if not other.org_uri:
            return False
        return OrganizationReferencesObject.__eq_on_national_registry(
            self.org_uri, other.org_uri
        )

    def __eq_on_same_as(self, other: "OrganizationReferencesObject"):
        if not self.same_as:
            return False
        if not other.same_as:
            return False
        else:
            matches = [org for org in self.same_as if org in other.same_as]
            return len(matches) > 0

    @staticmethod
    def __eq_on_http(uri_1: str, uri_2: str) -> bool:
        if NATIONAL_REGISTRY_PATTERN in uri_1 and NATIONAL_REGISTRY_PATTERN in uri_2:
            return OrganizationReferencesObject.__eq_on_national_registry(uri_1, uri_2)
        suffix_1 = uri_1.split("//")[1]
        suffix_2 = uri_2.split("//")[1]
        return suffix_1 == suffix_2

    @staticmethod
    def __eq_on_national_registry(uri_1: str, uri_2: str) -> bool:
        suffix_1 = uri_1.split("/")
        suffix_2 = uri_2.split("/")
        return suffix_1[-1] == suffix_2[-1]

    @staticmethod
    def from_organization_catalog_single_response(organization: dict):
        return OrganizationReferencesObject(
            org_uri=organization[OrgCatalogKeys.URI],
            org_path=organization[OrgCatalogKeys.ORG_PATH],
            name=organization[OrgCatalogKeys.NAME],
        )

    @staticmethod
    def from_organization_catalog_list_response(organizations: List[dict]):
        return [
            OrganizationReferencesObject.from_organization_catalog_single_response(org)
            for org in organizations
        ]

    @staticmethod
    def from_sparql_query_result(organization: dict) -> "OrganizationReferencesObject":
        keys = organization.keys()
        if ContentKeys.ORG_NAME in keys:
            name = organization.get(ContentKeys.ORG_NAME).get(ContentKeys.VALUE)
        else:
            name = ""

        reference_object = OrganizationReferencesObject(name=name)
        if ContentKeys.PUBLISHER in keys:
            publisher_uri = organization.get(ContentKeys.PUBLISHER).get(
                ContentKeys.VALUE
            )
            if OrganizationReferencesObject.is_national_registry_uri(publisher_uri):
                reference_object.org_uri = publisher_uri
            else:
                reference_object.same_as.append(publisher_uri)
        if ContentKeys.SAME_AS in keys:
            same_as_uri = organization.get(ContentKeys.SAME_AS).get(ContentKeys.VALUE)
            if OrganizationReferencesObject.is_national_registry_uri(same_as_uri):
                reference_object.org_uri = same_as_uri
            else:
                reference_object.same_as.append(reference_object)
        return reference_object

    @staticmethod
    def from_dct_publisher(org_uri):
        if org_uri:
            if OrganizationReferencesObject.is_national_registry_uri(org_uri):
                return OrganizationReferencesObject(org_uri=org_uri)
            else:
                return OrganizationReferencesObject(same_as_entry=org_uri)
        else:
            return None

    @staticmethod
    def is_national_registry_uri(uri):
        if uri is None:
            return False
        prefix = uri.split(":")[1]
        return NATIONAL_REGISTRY_PATTERN in prefix

    @staticmethod
    def resolve_id(uri: str):
        if uri:
            uri_parts = uri.split("/")
            return uri_parts[-1]
        else:
            return None


class OrganizationStore:
    __instance__: "OrganizationStore" = None

    def __init__(self):
        if OrganizationStore.__instance__ is None:
            self.organizations: List = None
            OrganizationStore.__instance__ = self
        else:
            raise OrganizationStoreExistsException()

    def update(self, organizations: List[OrganizationReferencesObject] = None):
        if not self.organizations:
            self.organizations = organizations

    def add_organization(self, organization: OrganizationReferencesObject):
        if self.organizations is None:
            self.organizations = list()
        try:
            org_idx = self.organizations.index(organization)
        except ValueError:
            self.organizations.append(organization)
            org_idx = self.organizations.index(organization)
        if len(organization.same_as) > 0:
            self.organizations[org_idx].same_as.extend(organization.same_as)

    def get_orgpath(self, uri: str) -> str:
        try:
            org_idx = self.organizations.index(uri)
            return self.organizations[org_idx].org_path
        except ValueError:
            return None
        except AttributeError:
            raise OrganizationStoreNotInitiatedException()

    def get_organization(self, org) -> OrganizationReferencesObject:
        try:
            return self.organizations[self.organizations.index(org)]
        except ValueError:
            return None

    def add_all_publishers(self, publishers: List[dict]):
        for reference in publishers["results"]["bindings"]:
            self.add_organization(
                OrganizationReferencesObject.from_sparql_query_result(reference)
            )

    @staticmethod
    def get_instance() -> "OrganizationStore":
        if OrganizationStore.__instance__:
            return OrganizationStore.__instance__
        else:
            return OrganizationStore()


class OrganizationStoreExistsException(Exception):
    def __init__(self):
        self.message = "organization store is already created"


class OrganizationStoreNotInitiatedException(Exception):
    def __init__(self):
        self.message = "no content in OrganizationStore"
