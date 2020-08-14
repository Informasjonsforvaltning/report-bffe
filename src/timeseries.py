import asyncio

from src.responses import TimeSeriesResponse
from src.service_requests import fetch_dataset_time_series
from src.sparql_utils.sparql_parsers import parse_sparql_time_series
from src.utils import ServiceKey


def get_time_series(content_type: ServiceKey) -> TimeSeriesResponse:
    return time_series_functions[content_type]()


def get_dataset_time_series() -> TimeSeriesResponse:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    time_series = loop.run_until_complete(fetch_dataset_time_series())
    parsed_series = parse_sparql_time_series(time_series)
    return TimeSeriesResponse(parsed_series)


time_series_functions = {
    ServiceKey.DATA_SETS: get_dataset_time_series
}
