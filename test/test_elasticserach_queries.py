import pytest

from src.elasticsearch.queries import AggregationQuery
from src.utils import ServiceKey


@pytest.mark.unit
def test_aggregation_query_with_organization_id_filter():
    result = AggregationQuery(
        report_type=ServiceKey.DATA_SETS,
        organization_id="1987634"
    )
    assert result.query
    assert result.query["bool"]["filter"][0] == {
        "term": {
            "orgId.keyword": {
                "value": "1987634"
            }
        }
    }
