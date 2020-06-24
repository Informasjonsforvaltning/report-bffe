import pytest

from src.utils import ServiceKey, NotAServiceKeyException


@pytest.mark.unit
def test_get_key():
    assert ServiceKey.get_key("informationmodels") == ServiceKey.INFO_MODELS
    assert ServiceKey.get_key("datasets") == ServiceKey.DATA_SETS
    assert ServiceKey.get_key("concepts") == ServiceKey.CONCEPTS
    assert ServiceKey.get_key("organizations") == ServiceKey.ORGANIZATIONS
    assert ServiceKey.get_key("dataservices") == ServiceKey.DATA_SERVICES
    with pytest.raises(NotAServiceKeyException):
        ServiceKey.get_key("notakey")
