import pytest

from fdk_reports_bff.responses import (
    ConceptResponse,
    DataSetResponse,
    InformationModelResponse,
)
from fdk_reports_bff.service.utils import ThemeProfile
from test.unit_mock_data import concepts_aggregation, concepts_in_use


@pytest.mark.unit
def test_information_model_response():
    es_result = {
        "_embedded": {"informationmodels": []},
        "page": {"totalElements": 574, "totalPages": 58, "number": 0},
        "aggregations": {
            "orgPath": {
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
                "buckets": [
                    {"key": "/ANNET", "doc_count": 794},
                    {"key": "/ANNET/910298062", "doc_count": 642},
                    {"key": "/STAT", "doc_count": 466},
                    {"key": "/STAT/972417858", "doc_count": 112},
                    {"key": "/STAT/972417858/971040238", "doc_count": 109},
                    {"key": "/STAT/972417874", "doc_count": 100},
                ],
            },
            "firstHarvested": {
                "buckets": [
                    {"key": "last30days", "count": 96},
                    {"key": "last365days", "count": 4267},
                    {"key": "last7days", "count": 3},
                ]
            },
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
def test_dataset_with_theme_profile():
    result = DataSetResponse(
        total=21,
        catalogs=[
            {"key": "/STAT/912660680/970188290", "count": 17},
            {"key": "/STAT/972417904/874783242", "count": 15},
            {"key": "/KOMMUNE/958935420", "count": 13},
        ],
        org_paths=[
            {"key": "/STAT/912660680/970188290", "count": 17},
            {"key": "/STAT/972417904/874783242", "count": 15},
            {"key": "/KOMMUNE/958935420", "count": 13},
        ],
        access_rights=[],
        themes=[
            {"key": "trafikk-og-transport", "count": 112},
            {"key": "familie-og-barn", "count": 108},
            {"key": "naring", "count": 105},
            {"key": "naring/landbruk", "count": 98},
            {"key": "bygg-og-eiendom", "count": 97},
            {"key": "bygg-og-eiendom", "count": 97},
            {"key": "trafikk-og-transport/mobilitetstilbud", "count": 97},
            {"key": "trafikk-og-transport/trafikkinformasjon", "count": 97},
            {"key": "trafikk-og-transport/veg-og-vegregulering", "count": 97},
            {"key": "trafikk-og-transport/yrkestransport", "count": 97},
        ],
        with_subject=19,
        opendata=3,
        new_last_week=1,
        national_component=2,
        dist_formats=[],
        theme_profile=ThemeProfile.TRANSPORT,
        organization_count=5,
    )

    assert len(result.themesAndTopicsCount) == 4
    assert len(result.catalogs) == 3
    assert result.totalObjects == 21
    assert result.withSubject == 19
    assert result.organizationCount == 5
