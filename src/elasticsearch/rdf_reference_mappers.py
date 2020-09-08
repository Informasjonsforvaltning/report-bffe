from typing import List

from src.elasticsearch.queries import CATALOG_RECORD_AGGREGATION_FIELDS
from src.rdf_namespaces import JSON_LD, ContentKeys


class CatalogRecords:
    def __init__(self, record_entry):
        self.uri = record_entry[0]
        content = record_entry[1]
        content_keys = content.keys()
        self.json_rdf_entry = record_entry
        if JSON_LD.DCT.isPartOf in content_keys:
            self.is_part_of = content.get(JSON_LD.DCT.isPartOf)[0][ContentKeys.VALUE]
        self.primary_topic = content.get(JSON_LD.FOAF.primaryTopic)[0][ContentKeys.VALUE]
        self.issued = content.get(JSON_LD.DCT.issued)[0][ContentKeys.VALUE]

    def primary_topic_is(self, uri) -> bool:
        return self.primary_topic == uri


class CatalogReference:
    def __init__(self, catalog_entry: tuple, catalog_records: List[CatalogRecords]):
        catalog_entry_content = catalog_entry[1]
        self.name = catalog_entry_content[JSON_LD.DCT.title][0][ContentKeys.VALUE]
        self.uri = catalog_entry[0]
        self.record_refs = [record.uri for record in catalog_records if record.primary_topic_is(self.uri)]
        if JSON_LD.DCAT.dataset in catalog_entry_content.keys():
            self.datasets = [val[ContentKeys.VALUE] for val in catalog_entry_content.get(JSON_LD.DCAT.dataset)]
        else:
            self.datasets = list()

    def __eq__(self, other):
        if type(other) == str:
            eq_str = other.strip()
            return eq_str == self.uri or eq_str in self.datasets or eq_str in self.record_refs


class RdfReferenceMapper:
    def __init__(self, document_list):
        self.catalog_records = [CatalogRecords(entry) for entry in document_list if
                                JSON_LD.rdf_type_equals(JSON_LD.DCAT.CatalogRecord, entry)]
        self.catalogs = [CatalogReference(catalog_entry=entry,
                                          catalog_records=self.catalog_records)
                         for entry in document_list if JSON_LD.rdf_type_equals(JSON_LD.DCAT.type_catalog, entry)]

    def get_dataset_catalog_name(self, record_part_of_uri: str = None, dataset_node_uri: str = None) -> str:
        from_dct_part_of = self.__get_catalog_name_by_dct_part_of(record_part_of_uri)
        if from_dct_part_of is not None:
            return from_dct_part_of
        else:
            try:
                catalog_idx = self.catalogs.index(dataset_node_uri)
                catalog = self.catalogs[catalog_idx]
                return catalog.name
            except ValueError:
                return None

    def __get_catalog_name_by_dct_part_of(self, record_part_of_uri: str):
        if record_part_of_uri is not None:
            try:
                catalog_idx = self.catalogs.index(record_part_of_uri)
                catalog = self.catalogs[catalog_idx]
                return catalog.name
            except ValueError:
                return None
        else:
            return None

    def get_catalog_record_for_dataset(self, dataset_uri) -> dict:
        for record in self.catalog_records:
            if record.primary_topic_is(dataset_uri):
                return reduce_record(record.json_rdf_entry)


def reduce_record(record: dict):
    reduced_record = record[1].copy()
    for items in record[1].items():
        key = items[0]
        if key not in CATALOG_RECORD_AGGREGATION_FIELDS:
            reduced_record.pop(key)
    return reduced_record
