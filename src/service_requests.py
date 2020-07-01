import os

from src.utils import ServiceKey

service_urls = {
    ServiceKey.ORGANIZATIONS: os.getenv('ORGANIZATION_CATALOG_URL') or "http://localhost:8080/organizations",
    ServiceKey.INFO_MODELS: os.getenv('INFORMATIONMODELS_HARVESTER_URL') or "http://localhost:8080/informationmodels",
    ServiceKey.DATA_SERVICES: os.getenv('DATASERVICE_HARVESTER_URL') or "http://localhost:8080/apis",
    ServiceKey.DATA_SETS: os.getenv('DATASET_HARVESTER_URL') or "http://localhost:8080/datasets",
    ServiceKey.CONCEPTS: os.getenv('CONCEPT_HARVESTER_URL') or "http://localhost:8080/concepts"
}


# from organization catalog !important
async def get_organizations_from_catalog() -> list:
    pass


async def get_organization_from_catalog(national_reg_id: str) -> dict:
    pass


# from reference data (called seldom, not a crisis if they're slow) !important
async def get_themes_and_topics_from_service():
    pass


async def get_access_rights():
    pass


async def get_los_paths():
    pass


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


# datasets !important
async def get_datasets_statistics():
    # see datasets_simple_aggs_response in unit_mock_data.py for expected result
    pass


async def get_datasets_access_rights():
    # see datasets_access_rights in unit_mock_data.py for expected result
    pass


async def get_datasets_themes_and_topics():
    # see datasets_themes_and_topics in unit_mock_data.py for expected result
    pass


async def get_dataset_time_series():
    # see timeseries in unit_mock_data.py for expected result
    pass
