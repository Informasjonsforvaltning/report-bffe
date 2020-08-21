import asyncio

from src.responses import TimeSeriesResponse
from src.utils import ServiceKey


def get_time_series(content_type: ServiceKey) -> TimeSeriesResponse:
    return time_series_functions[content_type]()


def get_dataset_time_series() -> TimeSeriesResponse:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        return None
time_series_functions = {
    ServiceKey.DATA_SETS: get_dataset_time_series
}
