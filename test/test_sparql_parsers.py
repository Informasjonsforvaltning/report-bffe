import pytest

from src.sparql_parsers import parse_sparql_formats_count, parse_sparql_single_results, ContentKeys, \
    parse_sparql_catalogs_count, parse_sparql_access_rights_count, parse_sparql_time_series, \
    parse_sparql_themes_and_topics
from test.unit_mock_data import datasets_format_count, datasets_simple_aggs_response, datasets_catalogs, \
    datasets_access_rights, mocked_org_paths, mocked_access_rights, time_series


@pytest.mark.unit
def test_parse_formats_json_sparql_for_datasets():
    result = parse_sparql_formats_count(sparql_result=datasets_format_count)
    assert len(result) == 6
    assert [x["count"] for x in result if x["key"] == "JSON"][0] == 20
    assert [x["count"] for x in result if x["key"] == "CSV"][0] == 20
    assert [x["count"] for x in result if x["key"] == "KML"][0] == 48
    assert [x["count"] for x in result if x["key"] == "PNG"][0] == 3


@pytest.mark.unit
def test_parse_sparql_single_result():
    result = parse_sparql_single_results(sparql_results=datasets_simple_aggs_response)
    assert result[ContentKeys.TOTAL] == "508"
    assert result[ContentKeys.NATIONAL_COMPONENT] == "50"
    assert result[ContentKeys.NEW_LAST_WEEK] == "8"
    assert result[ContentKeys.WITH_SUBJECT] == "76"


@pytest.mark.unit
def test_parse_sparql_catalogs_count(mock_get_org_path):
    result = parse_sparql_catalogs_count(sparql_result=datasets_catalogs)
    assert (result.__len__()) == 3
    assert [x["count"] for x in result if x["key"] == "STAT/912660680/974760673"][0] == 6
    assert [x["count"] for x in result if x["key"] == "STAT/972417858/991825827"][0] == 7
    assert [x["count"] for x in result if x["key"] == "STAT/912660680/917422575"][0] == 103


@pytest.mark.unit
def test_parse_sparql_time_series():
    result = parse_sparql_time_series(time_series)
    assert result.__len__() == 4
    for month in result:
        keys = month.keys()
        assert 'xAxis' in keys
        assert 'yAxis' in keys
        assert month['yAxis'].isdigit()


@pytest.mark.unit
def test_parse_sparql_access_rights_count(mock_get_ar_code):
    result = parse_sparql_access_rights_count(datasets_access_rights)
    assert result.__len__() == 3
    assert [x["count"] for x in result if x["key"] == "PUBLIC"][0] == 88
    assert [x["count"] for x in result if x["key"] == "NON_PUBLIC"][0] == 76
    assert [x["count"] for x in result if x["key"] == "RESTRICTED"][0] == 35


@pytest.mark.unit
def test_parse_sparql_themes_and_topics():
    pass


@pytest.fixture
def mock_get_org_path(mocker):
    mocker.patch('src.sparql_parsers.get_org_path', side_effect=mocked_org_paths)


@pytest.fixture
def mock_get_ar_code(mocker):
    mocker.patch('src.sparql_parsers.get_access_rights_code', side_effect=mocked_access_rights)


@pytest.fixture
def mock_get_themes_and_topics():
    result = None
