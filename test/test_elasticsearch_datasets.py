import pytest

from src.elasticsearch.datasets import insert_datasets


@pytest.mark.unit
def test_dry_run():
    insert_datasets()