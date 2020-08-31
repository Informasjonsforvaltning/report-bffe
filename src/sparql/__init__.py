from src.sparql.builder import encode_for_sparql
from src.sparql.queries import build_dataset_publisher_query


def get_dataset_publisher_query():
    return encode_for_sparql(build_dataset_publisher_query())
