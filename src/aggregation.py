import asyncio

from src.service_requests import get_datasets_statistics, get_datasets_access_rights, get_datasets_themes_and_topics
from src.utils import ServiceKey


def get_report(report_fun):
    return report_fun()


def create_dataset_report():
    loop = asyncio.get_event_loop()
    dataset_content_requests = asyncio.gather(
        get_datasets_statistics(),
        get_datasets_access_rights(),
        get_datasets_themes_and_topics(),
    )
    simple_stats, access_rights, themes = loop.run_until_complete(dataset_content_requests)

    x = 0


report_functions = {
    ServiceKey.DATA_SETS: create_dataset_report
}
