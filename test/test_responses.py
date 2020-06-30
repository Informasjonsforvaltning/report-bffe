import pytest

from src.responses import InformationModelResponse, ConceptResponse
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
