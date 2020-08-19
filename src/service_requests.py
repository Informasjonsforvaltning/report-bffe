import os
from typing import List

from httpcore import ConnectError
from httpx import AsyncClient, ConnectTimeout, HTTPError

from src.sparql_utils import ContentKeys
from src.sparql_utils.datasets_sparql_queries import build_datasets_catalog_query, build_datasets_access_rights_query, \
    build_datasets_formats_query, build_datasets_themes_query, build_dataset_time_series_query, \
    build_dataset_simple_statistic_query
from src.utils import ServiceKey, FetchFromServiceException, NotInNationalRegistryException

service_urls = {
    ServiceKey.ORGANIZATIONS: os.getenv('ORGANIZATION_CATALOG_URL') or "http://localhost:8080/organizations",
    ServiceKey.INFO_MODELS: os.getenv('INFORMATIONMODELS_HARVESTER_URL') or "http://localhost:8080/informationmodels",
    ServiceKey.DATA_SERVICES: os.getenv('DATASERVICE_HARVESTER_URL') or "http://localhost:8080/apis",
    ServiceKey.DATA_SETS: os.getenv('DATASET_HARVESTER_URL') or "http://localhost:8080",
    ServiceKey.CONCEPTS: os.getenv('CONCEPT_HARVESTER_URL') or "http://localhost:8080/concepts",
    ServiceKey.REFERENCE_DATA: f"{os.getenv('REFERENCE_DATA_URL')}" or "http://localhost:8080/reference-data"
}

sparql_select_url = "sparql/select"
meta_sparql_select_url = "/sparql/meta/select"
default_headers = {
    'accept': 'application/json'
}

organization_cache_key = "organizations"


async def fetch_organizations_from_organizations_catalog() -> List[dict]:
    url: str = f'{service_urls.get(ServiceKey.ORGANIZATIONS)}/organizations'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout) as err:
            raise FetchFromServiceException(
                execution_point="organizations",
                url=url
            )


async def fetch_organization_from_catalog(national_reg_id: str, name: str) -> dict:
    url: str = f'{service_urls.get(ServiceKey.ORGANIZATIONS)}/organizations/{national_reg_id}'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()

            return response.json()
        except (ConnectError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="get organization by id",
                url=url
            )
        except HTTPError as err:
            if err.response.status_code == 404:
                return await attempt_fetch_organization_by_name_from_catalog(name)
            else:
                raise FetchFromServiceException(
                    execution_point=f"{err.response.status_code}: get organization",
                    url=url
                )


async def attempt_fetch_organization_by_name_from_catalog(name: str) -> dict:
    url: str = f'{service_urls.get(ServiceKey.ORGANIZATIONS)}/organizations?name={name.upper()}'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()
            return response.json()[0]
        except (ConnectError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="get organization by name",
                url=url
            )
        except HTTPError as err:
            if err.response.status_code == 404:
                raise NotInNationalRegistryException(name)
            else:
                raise FetchFromServiceException(
                    execution_point=f"{err.response.status_code}: get organization",
                    url=url
                )
        except IndexError:
            raise NotInNationalRegistryException(name)


async def get_generated_org_path_from_organization_catalog(name: str):
    pass


# from reference data (called seldom, not a crisis if they're slow) !important
async def fetch_themes_and_topics_from_reference_data() -> List[dict]:
    url = f'{service_urls.get(ServiceKey.REFERENCE_DATA)}/los'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, timeout=5)
            response.raise_for_status()
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="reference-data themes and topics",
                url=url
            )


async def fetch_access_rights_from_reference_data():
    url = f'{service_urls.get(ServiceKey.REFERENCE_DATA)}/codes/rightsstatement'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, timeout=5)
            response.raise_for_status()
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="reference-data get access rights",
                url=url
            )


# datasets

async def fetch_datasets_catalog(org_uris: List[str] = None, theme: List[str] = None):
    url = f'{service_urls.get(ServiceKey.DATA_SETS)}/{sparql_select_url}?query={build_datasets_catalog_query(org_uris, theme)} '
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()
            if response.status_code == 204:
                return {}
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="datasets catalog query",
                url=url
            )


async def query_simple_statistic(field: ContentKeys, org_uris: List[str] = None, theme=None):

    query = build_dataset_simple_statistic_query(field, org_uris=org_uris, theme=theme)
    if field == ContentKeys.NEW_LAST_WEEK:
        base_url = f"{service_urls.get(ServiceKey.DATA_SETS)}/{meta_sparql_select_url}"
    else:
        base_url = f"{service_urls.get(ServiceKey.DATA_SETS)}/{sparql_select_url}"
    url = f'{base_url}?query={query}'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()
            if response.status_code == 204:
                return {}
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="datasets total query",
                url=url
            )


async def get_datasets_access_rights(orgpath, theme):
    url = f'{service_urls.get(ServiceKey.DATA_SETS)}/{sparql_select_url}?query={build_datasets_access_rights_query(orgpath, theme)}'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="datasets access_rights query",
                url=url
            )


async def get_datasets_themes_and_topics(org_uris: List[str] = None, theme=None):
    url = f'{service_urls.get(ServiceKey.DATA_SETS)}/{sparql_select_url}?query={build_datasets_themes_query(org_uris, theme)} '
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="datasets formats query",
                url=url
            )


async def get_datasets_formats(orgpath, theme):
    url = f'{service_urls.get(ServiceKey.DATA_SETS)}/{sparql_select_url}?query={build_datasets_formats_query(orgpath, theme)}'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="datasets formats query",
                url=url
            )


async def fetch_dataset_time_series():
    url = f'{service_urls.get(ServiceKey.DATA_SETS)}/{meta_sparql_select_url}?query={build_dataset_time_series_query()}'
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="datasets timeseries query",
                url=url
            )


# TODO
# informationmodels
async def get_informationmodels_statistic():
    # see informationmodels in unit_mock_data.py for expected result
    pass


# concepts
async def get_concepts_in_use():
    # see concepts_in_user in unit_mock_data.py for expected result
    pass


async def get_concepts_statistics():
    # see concepts_aggregation in unit_mock_data.py for expected result
    pass
