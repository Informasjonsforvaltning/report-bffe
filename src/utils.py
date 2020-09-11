from datetime import datetime
from typing import List
from dateutil import parser


class ContentKeys:
    SAME_AS = "sameAs"
    PUBLISHER = "publisher"
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
    LOS_PATH = "losPath"
    CATALOGS = "catalogs"
    ORGANIZATION_COUNT = "organizationCount"


class OrgCatalogKeys:
    NAME = "name"
    URI = "norwegianRegistry"
    ORG_PATH = "orgPath"


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


NATIONAL_REGISTRY_PATTERN = "data.brreg.no/enhetsregisteret"


class ParsedDataPoint:
    def __init__(self, es_bucket=None, month=None, year=None, last_month_count=0):
        if es_bucket is not None:
            self.y_axis = es_bucket["doc_count"] + last_month_count
            self.x_axis = es_bucket["key_as_string"]
            self.month, self.year = self.parse_date()
        else:
            self.y_axis = last_month_count
            next_date = None
            if month < 10:
                next_date = f"01.0{month}.{year}"
            else:
                next_date = f"01.{month}.{year}"

            self.x_axis = datetime.strptime(next_date, '%d.%m.%Y').isoformat() + ".000Z"
            self.year = year
            self.month = month

    def response_dict(self):
        return {
            ContentKeys.TIME_SERIES_Y_AXIS: self.y_axis,
            ContentKeys.TIME_SERIES_X_AXIS: self.x_axis
        }

    def parse_date(self):
        date = parser.parse(self.x_axis)
        return date.month, date.year

    def get_next_month(self):
        next_month = self.month + 1
        next_year = self.year
        if next_month == 13:
            next_month = 1
            next_year += 1
        return ParsedDataPoint(month=next_month, year=next_year, last_month_count=self.y_axis)

    def __eq__(self, other: 'ParsedDataPoint'):
        return self.month == other.month and self.year == other.year

    @staticmethod
    def from_date_time(date: datetime, last_data_point: 'ParsedDataPoint'):
        return ParsedDataPoint(month=date.month, year=date.year, last_month_count=last_data_point.y_axis)


class ThemeProfile:
    TRANSPORT = "transport"
    TRANSPORT_THEMES = ["trafikk-og-transport/mobilitetstilbud", "trafikk-og-transport/trafikkinformasjon",
                        "trafikk-og-transport/veg-og-vegregulering", "trafikk-og-transport/yrkestransport"]


class QueryParameter:
    ORGANIZATION_ID = "organizationId"
    THEME_PROFILE = "themeprofile"
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


class NoOrganizationEntriesException(Exception):
    def __init__(self):
        self.reason = f"organization store is empty"


class StartSchedulerError(Exception):
    def __init__(self, hosts=List[dict]):
        self.message = f"Failed to contact ElasticSearch when attempting to start scheduler.\n hosts: {hosts} "
