import pytest

from src.sparql_utils.sparql_parsers import parse_sparql_formats_count, parse_sparql_catalogs_count, \
    parse_sparql_time_series, parse_sparql_themes_and_topics_count, \
    parse_sparql_single_results, ContentKeys, parse_sparql_access_rights_count, ParsedDataPoint
from test.unit_mock_data import datasets_format_count, datasets_simple_aggs_response, datasets_catalogs, \
    datasets_access_rights, mocked_org_paths, mocked_access_rights, dataset_time_series, datasets_themes_and_topics, \
    mocked_los_paths


@pytest.mark.unit
def test_parse_formats_json_sparql_for_datasets(event_loop):
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
def test_parse_sparql_catalogs_count(event_loop, mock_get_org_path):
    result = event_loop.run_until_complete(parse_sparql_catalogs_count(sparql_result=datasets_catalogs))
    assert (result.__len__()) == 7
    assert [x["count"] for x in result if x["key"] == "/STAT"][0] == 6 + 7 + 103
    assert [x["count"] for x in result if x["key"] == "/STAT/912660680"][0] == 103 + 6
    assert [x["count"] for x in result if x["key"] == "/STAT/972417858"][0] == 7
    assert [x["count"] for x in result if x["key"] == "/STAT/912660680/974760673"][0] == 6
    assert [x["count"] for x in result if x["key"] == "/STAT/972417858/991825827"][0] == 7
    assert [x["count"] for x in result if x["key"] == "/STAT/912660680/917422575"][0] == 103


@pytest.mark.unit
def test_parse_sparql_access_rights_count(event_loop, mock_get_ar_code):
    result = event_loop.run_until_complete(parse_sparql_access_rights_count(datasets_access_rights))
    assert result.__len__() == 3
    assert [x["count"] for x in result if x["key"] == "PUBLIC"][0] == 88
    assert [x["count"] for x in result if x["key"] == "NON_PUBLIC"][0] == 76
    assert [x["count"] for x in result if x["key"] == "RESTRICTED"][0] == 35


@pytest.mark.unit
def test_parse_sparql_themes_and_topics(event_loop, mock_get_los_path):
    result = event_loop.run_until_complete(parse_sparql_themes_and_topics_count(datasets_themes_and_topics))
    assert result.__len__() == 6
    assert [x["count"] for x in result if x["key"] == "bygg-og-eiendom"][0] == 10 + 1 + 32
    assert [x["count"] for x in result if x["key"] == "bygg-og-eiendom/priser-og-gebyr-for-bygg-og-eiendom"][
               0] == 1 + 32
    assert [x["count"] for x in result if x["key"] == "bygg-og-eiendom/priser-og-gebyr-for-bygg-og-eiendom" \
                                                      "/renovasjonsavgift"][0] == 32
    assert [x["count"] for x in result if x["key"] == "natur-klima-og-miljo/avfallshandtering/kompostering"][0] == 2
    assert [x["count"] for x in result if x["key"] == "natur-klima-og-miljo/avfallshandtering"][0] == 2
    assert [x["count"] for x in result if x["key"] == "natur-klima-og-miljo"][0] == 2


@pytest.mark.unit
def test_parse_sparql_time_series():
    expected_series = [
        ParsedDataPoint(month=1, year=2020, count=2),
        ParsedDataPoint(month=4, year=2020, count=1),
        ParsedDataPoint(month=5, year=2020, count=1),
        ParsedDataPoint(month=6, year=2020, count=3)
    ]
    result = parse_sparql_time_series(dataset_time_series)
    assert len(result) == 4
    assert result[0] == expected_series[0]
    assert result[0].count == "1"
    assert result[1] == expected_series[1]
    assert result[1].count == "1"
    assert result[2] == expected_series[2]
    assert result[2].count == "1"
    assert result[3] == expected_series[3]
    assert result[3].count == "3"


@pytest.mark.unit
def test_parse_date_from_entry():
    input = {
        "month": {
            "type": "literal",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
            "value": "04"
        },
        "year": {
            "type": "literal",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
            "value": "2020"
        },
        "count": {
            "type": "literal",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
            "value": "1"
        }
    }

    result = ParsedDataPoint.from_result_entry(input)
    assert result == ParsedDataPoint(month=4, year=2020, count=768)


@pytest.mark.unit
def test_parsed_next_month():
    expect_may = ParsedDataPoint(month=5, year=2020, count=7)
    result = ParsedDataPoint(month=4, year=2020, count=7).get_next_month()
    assert result == expect_may
    expect_january = ParsedDataPoint(month=1, year=2012, count=2)
    result = ParsedDataPoint(month=12, year=2011,count=2).get_next_month()
    assert result == expect_january


@pytest.mark.unit
def test_parsed_date_str():
    input = {
        "month": {
            "type": "literal",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
            "value": "04"
        },
        "year": {
            "type": "literal",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
            "value": "2020"
        },
        "count": {
            "type": "literal",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
            "value": "1"
        }
    }

    result_from_entry = str(ParsedDataPoint.from_result_entry(input))
    result_from_init = str(ParsedDataPoint(month=7, year=1987, count=9))
    assert result_from_entry == "01.04.2020"
    assert result_from_init == "01.07.1987"


@pytest.mark.unit
def test_parsed_date_dict():
    input = {
        "month": {
            "type": "literal",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
            "value": "04"
        },
        "year": {
            "type": "literal",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
            "value": "2020"
        },
        "count": {
            "type": "literal",
            "datatype": "http://www.w3.org/2001/XMLSchema#integer",
            "value": "1"
        }
    }

    result_from_entry = ParsedDataPoint.from_result_entry(input).response_dict()
    assert result_from_entry["xAxis"] == "01.04.2020"
    assert result_from_entry["yAxis"] == "1"


@pytest.fixture
def mock_get_org_path(mocker):
    mocker.patch('src.sparql_utils.sparql_parsers.get_org_path', side_effect=mocked_org_paths)


@pytest.fixture
def mock_get_ar_code(mocker):
    mocker.patch('src.sparql_utils.sparql_parsers.get_access_rights_code', side_effect=mocked_access_rights)


@pytest.fixture
def mock_get_los_path(mocker):
    mocker.patch('src.sparql_utils.sparql_parsers.get_los_path', side_effect=mocked_los_paths)
