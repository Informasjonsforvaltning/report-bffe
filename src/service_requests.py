import os
import urllib.parse
from typing import List

from httpcore import ConnectError
from httpx import AsyncClient, ConnectTimeout, HTTPError

from src.sparql import (
    get_dataservice_publisher_query,
    get_dataservice_query,
    get_dataset_publisher_query,
)
from src.utils import (
    ContentKeys,
    FetchFromServiceException,
    NotInNationalRegistryException,
    ServiceKey,
)

service_urls = {
    ServiceKey.ORGANIZATIONS: os.getenv("ORGANIZATION_CATALOG_URL")
    or "http://localhost:8080",
    ServiceKey.INFO_MODELS: os.getenv("INFORMATIONMODELS_HARVESTER_URL")
    or "http://localhost:8080",
    ServiceKey.DATA_SERVICES: os.getenv("FDK_BASE") or "http://localhost:8080",
    ServiceKey.DATA_SETS: os.getenv("DATASET_HARVESTER_URL") or "http://localhost:8080",
    ServiceKey.CONCEPTS: os.getenv("CONCEPT_HARVESTER_URL") or "http://localhost:8080",
    ServiceKey.REFERENCE_DATA: os.getenv("REFERENCE_DATA_URL")
    or "http://localhost:8080/reference-data",
    ServiceKey.FDK_BASE: os.getenv("FDK_BASE") or "http://localhost:8080",
}

default_headers = {"accept": "application/json"}


async def fetch_organizations_from_organizations_catalog() -> List[dict]:
    url: str = f"{service_urls.get(ServiceKey.ORGANIZATIONS)}/organizations"
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(execution_point="organizations", url=url)


async def fetch_organization_from_catalog(national_reg_id: str, name: str) -> dict:
    url: str = (
        f"{service_urls.get(ServiceKey.ORGANIZATIONS)}/organizations/{national_reg_id}"
    )
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, headers=default_headers, timeout=5)
            response.raise_for_status()

            return response.json()
        except (ConnectError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="get organization by id", url=url
            )
        except (ConnectTimeout, ConnectError):
            raise FetchFromServiceException(
                execution_point="connection error to organization catalog", url=url
            )
        except HTTPError as err:
            if err.response.status_code == 404:
                return await attempt_fetch_organization_by_name_from_catalog(name)
            else:
                raise FetchFromServiceException(
                    execution_point=f"{err.response.status_code}: get organization",
                    url=url,
                )


async def attempt_fetch_organization_by_name_from_catalog(name: str) -> dict:
    if name is None:
        raise NotInNationalRegistryException("No name")
    url: str = f"{service_urls.get(ServiceKey.ORGANIZATIONS)}/organizations"
    async with AsyncClient() as session:
        try:
            response = await session.get(
                url=url,
                headers=default_headers,
                params={"name": name.upper()},
                timeout=5)
            response.raise_for_status()
            return response.json()[0]
        except (ConnectError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="get organization by name", url=url
            )
        except HTTPError as err:
            if err.response.status_code == 404:
                raise NotInNationalRegistryException(name)
            else:
                raise FetchFromServiceException(
                    execution_point=f"{err.response.status_code}: get organization",
                    url=url,
                )
        except IndexError:
            raise NotInNationalRegistryException(name)


async def fetch_generated_org_path_from_organization_catalog(name: str):
    if name is None:
        return None
    url: str = f"{service_urls.get(ServiceKey.ORGANIZATIONS)}/organizations/orgpath/{name.upper()}"
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, timeout=5)
            response.raise_for_status()
            return response.text
        except (ConnectError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="get organization by name", url=url
            )
        except HTTPError as err:
            raise FetchFromServiceException(
                execution_point=f"{err.response.status_code}: get organization", url=url
            )


# from reference data (called seldom, not a crisis if they're slow) !important
async def fetch_themes_and_topics_from_reference_data() -> List[dict]:
    url = f"{service_urls.get(ServiceKey.REFERENCE_DATA)}/los"
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, timeout=5)
            response.raise_for_status()
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="reference-data themes and topics", url=url
            )


async def fetch_open_licences_from_reference_data() -> List[dict]:
    url = f"{service_urls.get(ServiceKey.REFERENCE_DATA)}/codes/openlicenses"
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, timeout=5)
            response.raise_for_status()
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="reference-data themes and topics", url=url
            )


async def fetch_access_rights_from_reference_data():
    url = f"{service_urls.get(ServiceKey.REFERENCE_DATA)}/codes/rightsstatement"
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, timeout=5)
            response.raise_for_status()
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="reference-data get access rights", url=url
            )


async def fetch_media_types_from_reference_data():
    url = f"{service_urls.get(ServiceKey.REFERENCE_DATA)}/codes/mediatypes"
    async with AsyncClient() as session:
        try:
            response = await session.get(url=url, timeout=5)
            response.raise_for_status()
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="reference-data get mediatypes rights", url=url
            )


async def fetch_catalog_from_dataset_harvester() -> dict:
    url = f"{service_urls.get(ServiceKey.DATA_SETS)}/catalogs"
    async with AsyncClient() as session:
        try:
            response = await session.get(
                url=url,
                headers={"Accept": "application/rdf+json"},
                params={"catalogrecords": "true"},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="fetching dataset catalog", url=url
            )


async def fetch_publishers_from_dataset_harvester() -> dict:
    publisher_query = urllib.parse.quote_plus(get_dataset_publisher_query())
    url = f"{service_urls.get(ServiceKey.FDK_BASE)}/sparql"
    async with AsyncClient() as session:
        try:
            response = await session.get(
                url=url,
                headers=default_headers,
                params={"query": publisher_query},
                timeout=60)
            response.raise_for_status()
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="fetching publishers from dataset catalog", url=url
            )


# informationmodels
async def get_informationmodels_statistic():
    async with AsyncClient() as session:
        try:
            informationmodels: List = []
            page_number = 0
            while True:
                url: str = (
                    f"{service_urls.get(ServiceKey.INFO_MODELS)}/informationmodels"
                )

                response = await session.post(url=url, json={"page": page_number})
                page_count = response.json()[ContentKeys.PAGE_OBJECT][
                    ContentKeys.TOTAL_PAGES
                ]
                informationmodels.extend(response.json()[ContentKeys.HITS])

                if page_count - 1 == page_number:
                    break
                page_number += 1

            return informationmodels

        except HTTPError:
            raise FetchFromServiceException(
                execution_point="fetching informationmodels", url=url
            )


# concepts
async def fetch_all_concepts():
    async with AsyncClient() as session:
        try:
            concepts: List = []
            page_number = 0
            while True:
                url: str = f"{service_urls.get(ServiceKey.CONCEPTS)}/concepts"
                response = await session.get(
                    url=url,
                    params={
                        "returnfields": "publisher,prefLabel,harvest",
                        "size": "1000",
                        "page": page_number,
                    },
                    timeout=5,
                )
                page_count = response.json()[ContentKeys.PAGE_OBJECT][
                    ContentKeys.TOTAL_PAGES
                ]
                concepts.extend(
                    response.json()[ContentKeys.EMBEDDED][ContentKeys.CONCEPTS]
                )
                if page_count - 1 == page_number:
                    break
                page_number += 1

            return concepts

        except HTTPError:
            raise FetchFromServiceException(
                execution_point="fetching concepts", url=url
            )


# dataservices
async def fetch_dataservices() -> dict:
    dataservice_query = urllib.parse.quote_plus(get_dataservice_query())
    url = f"{service_urls.get(ServiceKey.FDK_BASE)}/sparql"
    async with AsyncClient() as session:
        try:
            response = await session.get(
                url=url,
                headers=default_headers,
                params={"query": dataservice_query},
                timeout=60)
            response.raise_for_status()
            res_json = response.json()
            sparql_bindings = res_json[ContentKeys.SPARQL_RESULTS][
                ContentKeys.SPARQL_BINDINGS
            ]
            return sparql_bindings
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="fetching dataservices catalog", url=url
            )


async def fetch_publishers_from_dataservice() -> dict:
    publisher_query = urllib.parse.quote_plus(get_dataservice_publisher_query())
    url = f"{service_urls.get(ServiceKey.FDK_BASE)}/sparql"
    async with AsyncClient() as session:
        try:
            response = await session.get(
                url=url,
                headers=default_headers,
                params={"query": publisher_query},
                timeout=60)
            response.raise_for_status()
            return response.json()
        except (ConnectError, HTTPError, ConnectTimeout):
            raise FetchFromServiceException(
                execution_point="fetching publishers from dataservice catalog", url=url
            )
