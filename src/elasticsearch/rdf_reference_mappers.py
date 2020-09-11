from typing import List

from src.elasticsearch.queries import CATALOG_RECORD_AGGREGATION_FIELDS, EsMappings
from src.elasticsearch.utils import get_values_from_nested_dict
from src.rdf_namespaces import JSON_RDF
from src.utils import ContentKeys


class CatalogRecords:
    def __init__(self, record_entry):
        self.uri = record_entry[0]
        content = record_entry[1]
        content_keys = content.keys()
        self.json_rdf_entry = record_entry
        if JSON_RDF.dct.isPartOf in content_keys:
            self.is_part_of = content.get(JSON_RDF.dct.isPartOf)[0][ContentKeys.VALUE]
        self.primary_topic = content.get(JSON_RDF.foaf.primaryTopic)[0][ContentKeys.VALUE]
        self.issued = content.get(JSON_RDF.dct.issued)[0][ContentKeys.VALUE]

    def primary_topic_is(self, uri) -> bool:
        return self.primary_topic == uri


class CatalogReference:
    def __init__(self, catalog_entry: tuple, catalog_records: List[CatalogRecords]):
        catalog_entry_content = catalog_entry[1]
        self.name = catalog_entry_content[JSON_RDF.dct.title][0][ContentKeys.VALUE]
        self.uri = catalog_entry[0]
        self.record_refs = [record.uri for record in catalog_records if record.primary_topic_is(self.uri)]
        if JSON_RDF.dcat.dataset in catalog_entry_content.keys():
            self.datasets = [val[ContentKeys.VALUE] for val in catalog_entry_content.get(JSON_RDF.dcat.dataset)]
        else:
            self.datasets = list()

    def __eq__(self, other):
        if type(other) == str:
            eq_str = other.strip()
            return eq_str == self.uri or eq_str in self.datasets or eq_str in self.record_refs


class RdfReferenceMapper:
    def __init__(self, document_list: List[dict], open_licenses: List[str]):
        self.catalog_records = [CatalogRecords(entry) for entry in document_list if
                                JSON_RDF.rdf_type_equals(JSON_RDF.dcat.CatalogRecord, entry)]
        self.catalogs = [CatalogReference(catalog_entry=entry,
                                          catalog_records=self.catalog_records)
                         for entry in document_list if JSON_RDF.rdf_type_equals(JSON_RDF.dcat.type_catalog, entry)]
        self.dct_licence_documents = [{entry[0]: entry[1]} for entry in document_list if
                                      JSON_RDF.rdf_type_in(JSON_RDF.dct.license_document, entry)]
        self.open_licenses = open_licenses
        self.open_license_b_nodes = self.get_open_license_nodes_from_license_docs()

    def has_open_license(self, dcat_distributions: List[dict], entry: dict) -> bool:
        for license_entry in dcat_distributions:
            try:
                licence_value = license_entry.get(JSON_RDF.dct.license)[0][ContentKeys.VALUE]
                if licence_value in self.open_licenses:
                    return True
                elif licence_value in self.open_license_b_nodes:
                    return True
            except TypeError:
                continue
        return False

    def get_open_license_nodes_from_license_docs(self) -> List[str]:
        source_values = [{"uri": list(licence_doc.items())[0][0],
                          ContentKeys.VALUE: get_values_from_nested_dict(licence_doc).get(JSON_RDF.dct.source)}
                         for licence_doc in self.dct_licence_documents]
        return [doc.get("uri") for doc in source_values if
                doc.get(ContentKeys.VALUE)[0][ContentKeys.VALUE] in self.open_licenses]

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

    def get_catalog_record_for_dataset(self, dataset_uri: str) -> dict:
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
