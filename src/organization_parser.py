from typing import List

from src.rdf_namespaces import OrgCatalogKeys, ContentKeys, JSON_LD
from src.utils import NATIONAL_REGISTRY_PATTERN


class OrganizationReferencesObject:
    def __init__(self, org_uri: str, org_path: str = None, same_as: str = None, name: str = None):
        self.org_uri: str = org_uri
        self.org_path: str = org_path
        self.same_as: str = same_as
        self.name: str = name

    def update_orgpath(self, org_path):
        self.org_path = org_path

    def update_same_as(self, foaf_same_as):
        self.same_as = foaf_same_as

    def has_national_registry_uri(self):
        prefix = self.org_uri.split(":")[1]
        return prefix == NATIONAL_REGISTRY_PATTERN

    def __eq__(self, other):
        if type(other) == OrganizationReferencesObject:
            same_uri = OrganizationReferencesObject.__eq_on_http(self.org_uri, other.org_uri)
            if same_uri:
                return True
            else:
                if self.same_as is not None:
                    return OrganizationReferencesObject.__eq_on_http(self.same_as, other.org_uri)
                else:
                    if other.same_as is not None:
                        return OrganizationReferencesObject.__eq_on_http(self.org_uri, other.same_as)
                    else:
                        return False
        elif type(other) == str:
            if other.startswith("http"):
                return OrganizationReferencesObject.__eq_on_http(self.org_uri, other)
            else:
                return False
        else:
            return False

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
        return suffix_1[- 1] == suffix_2[- 1]

    @staticmethod
    def from_organization_catalog_single_response(organization: dict):
        return OrganizationReferencesObject(
            org_uri=organization[OrgCatalogKeys.URI],
            org_path=organization[OrgCatalogKeys.ORG_PATH],
            name=organization[OrgCatalogKeys.NAME]
        )

    @staticmethod
    def from_organization_catalog_list_response(organizations: List[dict]):
        return [OrganizationReferencesObject.from_organization_catalog_single_response(org) for org in organizations]

    @staticmethod
    def from_json_ld_values(ld_org_uri_value: List[dict], ld_same_as_value: List[dict] = None):
        org_uri: str = ld_org_uri_value[0][ContentKeys.VALUE]
        same_as: str = None
        org_path: str = None
        if ld_same_as_value:
            same_as = ld_same_as_value[0][ContentKeys.VALUE]
        return OrganizationReferencesObject(org_uri, org_path, same_as)

    @staticmethod
    def is_national_registry_uri(uri):
        return NATIONAL_REGISTRY_PATTERN in uri

    @staticmethod
    def resolve_id(uri: str):
        uri_parts = uri.split("/")
        return uri_parts[-1]


class OrganizationStore:
    __instance__: 'OrganizationStore' = None

    def __init__(self):
        if OrganizationStore.__instance__ is None:
            self.organizations: List = None
            self.modified = False
            OrganizationStore.__instance__ = self
        else:
            raise OrganizationStoreExistsException()

    def update(self, organizations: List[OrganizationReferencesObject] = None):
        if not self.organizations:
            self.organizations = organizations

    def add_organization(self, organization: OrganizationReferencesObject):
        if not self.organizations:
            self.organizations = []
        if organization.org_uri not in [org.org_uri for org in self.organizations]:
            self.organizations.append(organization)
            self.modified = True

    def get_orgpath(self, uri: str) -> str:
        try:
            org_idx = self.organizations.index(uri)
            return self.organizations[org_idx].org_path
        except ValueError:
            return None
        except AttributeError:
            raise OrganizationStoreNotInitiatedException()

    @staticmethod
    def get_instance() -> 'OrganizationStore':
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
