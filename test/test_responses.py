import pytest

from src.responses import InformationModelResponse, ConceptResponse, TimeSeriesResponse
from src.sparql_utils.sparql_parsers import ParsedDataPoint
from test.unit_mock_data import concepts_aggregation, concepts_in_use


@pytest.mark.unit
def test_information_model_response():
    es_result = {
        "_embedded": {
            "informationmodels": []
        },
        "page": {
            "totalElements": 574,
            "totalPages": 58,
            "number": 0
        },
        "aggregations": {
            "orgPath": {
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
                "buckets": [
                    {
                        "key": "/ANNET",
                        "doc_count": 794
                    },
                    {
                        "key": "/ANNET/910298062",
                        "doc_count": 642
                    },
                    {
                        "key": "/STAT",
                        "doc_count": 466
                    },
                    {
                        "key": "/STAT/972417858",
                        "doc_count": 112
                    },
                    {
                        "key": "/STAT/972417858/971040238",
                        "doc_count": 109
                    },
                    {
                        "key": "/STAT/972417874",
                        "doc_count": 100
                    }
                ]
            },
            "firstHarvested": {
                "buckets": [
                    {
                        "key": "last30days",
                        "count": 96
                    },
                    {
                        "key": "last365days",
                        "count": 4267
                    },
                    {
                        "key": "last7days",
                        "count": 3
                    }
                ]
            }
        },
    }

    result = InformationModelResponse.from_es(es_result)

    assert result.totalObjects == 574
    assert result.newLastWeek == 3
    assert len(result.catalogs) == 6


@pytest.mark.unit
def test_concept_response():
    result = ConceptResponse.from_es(concepts_aggregation, concepts_in_use)
    assert len(result.mostInUse) == 3
    assert result.newLastWeek == 10
    assert len(result.catalogs) == 11


@pytest.mark.unit
def test_time_series_response():
    parsed_series = [
        ParsedDataPoint(month=11, year=2019, count=8),
        ParsedDataPoint(month=1, year=2020, count=2),
        ParsedDataPoint(month=4, year=2020, count=1),
        ParsedDataPoint(month=5, year=2020, count=1),
        ParsedDataPoint(month=6, year=2020, count=3)
    ]
    result = TimeSeriesResponse(parsed_series).json()
    assert len(result) == 10
    assert result[0]["xAxis"] == "01.11.2019"
    assert result[1]["xAxis"] == "01.12.2019"
    assert result[2]["xAxis"] == "01.01.2020"
    assert result[3]["xAxis"] == "01.02.2020"
    assert result[4]["xAxis"] == "01.03.2020"
    assert result[5]["xAxis"] == "01.04.2020"
    assert result[6]["xAxis"] == "01.05.2020"
    assert result[7]["xAxis"] == "01.06.2020"
    assert result[0]["yAxis"] == 8
    assert result[1]["yAxis"] == 0
    assert result[2]["yAxis"] == 2
    assert result[3]["yAxis"] == 0
    assert result[4]["yAxis"] == 0
    assert result[5]["yAxis"] == 1
    assert result[6]["yAxis"] == 1
    assert result[7]["yAxis"] == 3
