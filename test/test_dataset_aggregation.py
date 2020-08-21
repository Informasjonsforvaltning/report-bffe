import asyncio

import pytest

from src.dataset_aggregation import create_dataset_report
from src.responses import DataSetResponse


@pytest.mark.unit
def test_get_datasets(event_loop
                      ):
    asyncio.set_event_loop(event_loop)
    result: DataSetResponse = create_dataset_report(None, None, None)
    # assert 8 == len(result.catalogs)
    # assert 6 == len(result.formats)
    # assert 76 == int(result.withSubject)
    # assert 6 == int(result.opendata)
    # assert 508 == int(result.totalObjects)
    # assert 8 == int(result.newLastWeek)
    # assert 50 == int(result.nationalComponent)
    # assert 3 == len(result.accessRights)

