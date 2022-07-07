import pytest

from fdk_reports_bff.service.utils import (
    NotAServiceKeyException,
    ParsedDataPoint,
    ServiceKey,
)


@pytest.mark.unit
def test_get_key():
    assert ServiceKey.get_key("informationmodels") == ServiceKey.INFO_MODELS
    assert ServiceKey.get_key("datasets") == ServiceKey.DATA_SETS
    assert ServiceKey.get_key("concepts") == ServiceKey.CONCEPTS
    assert ServiceKey.get_key("organizations") == ServiceKey.ORGANIZATIONS
    assert ServiceKey.get_key("dataservices") == ServiceKey.DATA_SERVICES
    assert ServiceKey.get_key("new_reference_data") == ServiceKey.NEW_REFERENCE_DATA
    with pytest.raises(NotAServiceKeyException):
        ServiceKey.get_key("notakey")


@pytest.mark.unit
def test_get_next_month():
    es_bucket_november = {"key_as_string": "2019-11-01T00:00:00.000Z", "doc_count": 8}

    november = ParsedDataPoint(es_bucket=es_bucket_november)
    december = november.get_next_month()
    assert december.y_axis == 8


@pytest.mark.unit
def test_add_last_count_to_es_data_point():
    es_bucket_november = {"key_as_string": "2019-11-01T00:00:00.000Z", "doc_count": 8}

    november = ParsedDataPoint(es_bucket=es_bucket_november, last_month_count=112)
    assert november.y_axis == 120
