from typing import Any, List, Optional

from fdk_reports_bff.elasticsearch.queries import CATALOG_RECORD_AGGREGATION_FIELDS
from fdk_reports_bff.elasticsearch.utils import (
    get_values_from_nested_dict,
    map_formats_to_prefixed,
    strip_http_scheme,
)
from fdk_reports_bff.service.rdf_namespaces import JsonRDF
from fdk_reports_bff.service.referenced_data_store import FileTypes, MediaTypes
from fdk_reports_bff.service.utils import ContentKeys


class CatalogRecords:
    def __init__(self: Any, record_entry: Any) -> None:
        self.uri = record_entry[0]
        content = record_entry[1]
        content_keys = content.keys()
        self.json_rdf_entry = record_entry
        if JsonRDF.dct.isPartOf in content_keys:
            self.is_part_of = content.get(JsonRDF.dct.isPartOf)[0][ContentKeys.VALUE]
        self.primary_topic = content.get(JsonRDF.foaf.primaryTopic)[0][
            ContentKeys.VALUE
        ]
        self.issued = content.get(JsonRDF.dct.issued)[0][ContentKeys.VALUE]

    def primary_topic_is(self: Any, uri: Any) -> bool:
        return self.primary_topic == uri


class CatalogReference:
    def __init__(
        self: Any, catalog_entry: tuple, catalog_records: List[CatalogRecords]
    ) -> None:
        catalog_entry_content = catalog_entry[1]
        if JsonRDF.dct.title in catalog_entry_content:
            self.name = catalog_entry_content[JsonRDF.dct.title][0][ContentKeys.VALUE]
        self.uri = catalog_entry[0]
        self.record_refs = [
            record.uri
            for record in catalog_records
            if record.primary_topic_is(self.uri)
        ]
        if JsonRDF.dcat.dataset in catalog_entry_content.keys():
            self.datasets = [
                val[ContentKeys.VALUE]
                for val in catalog_entry_content.get(JsonRDF.dcat.dataset)
            ]
        else:
            self.datasets = list()

    def __eq__(self: Any, other: Any) -> bool:
        if type(other) == str:
            eq_str = other.strip()
            return (
                eq_str == self.uri
                or eq_str in self.datasets
                or eq_str in self.record_refs
            )
        else:
            return False


class RdfReferenceMapper:
    def __init__(
        self: Any,
        document_list: List,
        open_licenses: List[str],
        media_types: List[MediaTypes],
        file_types: List[FileTypes],
    ) -> None:
        self.media_types_dict = {}
        for media_type in media_types:
            self.media_types_dict[strip_http_scheme(media_type.uri)] = media_type

        self.file_types_dict = {}
        for file_type in file_types:
            self.file_types_dict[strip_http_scheme(file_type.uri)] = file_type

        self.catalog_records = [
            CatalogRecords(entry)
            for entry in document_list
            if JsonRDF.rdf_type_equals(JsonRDF.dcat.CatalogRecord, entry)
        ]
        self.catalogs = [
            CatalogReference(catalog_entry=entry, catalog_records=self.catalog_records)
            for entry in document_list
            if JsonRDF.rdf_type_equals(JsonRDF.dcat.type_catalog, entry)
        ]
        self.dct_licence_documents = [
            {entry[0]: entry[1]}
            for entry in document_list
            if JsonRDF.rdf_type_in(JsonRDF.dct.license_document, entry)
        ]
        self.open_licenses = open_licenses
        self.open_license_b_nodes = self.get_open_license_nodes_from_license_docs()
        self.distributions = [
            {entry[0]: entry[1]}
            for entry in document_list
            if JsonRDF.rdf_type_equals(JsonRDF.dcat.distribution_type, entry)
        ]

    def has_open_license(self: Any, dcat_distributions: List[dict]) -> bool:
        for license_entry in dcat_distributions:
            try:
                licenses = (
                    license_entry[JsonRDF.dct.license]
                    if license_entry.get(JsonRDF.dct.license)
                    else []
                )
                licence_value = (
                    licenses[0].get(ContentKeys.VALUE) if len(licenses) else None
                )
                if licence_value in self.open_licenses:
                    return True
                elif licence_value in self.open_license_b_nodes:
                    return True
            except TypeError:
                continue
        return False

    def get_distributions_in_entry(self: Any, entry: dict, node_uri: str) -> List:
        distribution_node_refs = [
            entry.get("value") for entry in entry[JsonRDF.dcat.distribution]
        ]
        ref_distribution_values = [
            get_values_from_nested_dict(node)
            for node in self.distributions
            if JsonRDF.node_uri_in(node, distribution_node_refs)
        ]

        if JsonRDF.node_uri_in({node_uri: node_uri}, distribution_node_refs):
            ref_distribution_values.append(remove_nested_distributions(entry))

        return ref_distribution_values

    def get_open_license_nodes_from_license_docs(self: Any) -> List[Any]:
        source_values = [
            {
                "uri": list(licence_doc.items())[0][0],
                ContentKeys.VALUE: get_values_from_nested_dict(licence_doc).get(
                    JsonRDF.dct.source
                ),
            }
            for licence_doc in self.dct_licence_documents
        ]
        nodes = []
        for doc in source_values:
            values = doc[ContentKeys.VALUE] if doc.get(ContentKeys.VALUE) else []
            lic_value = values[0].get(ContentKeys.VALUE) if len(values) > 0 else None
            if lic_value in self.open_licenses:
                nodes.append(doc.get("uri"))
        return nodes

    def get_dataset_catalog_name(
        self: Any,
        record_part_of_uri: Optional[str] = None,
        dataset_node_uri: Optional[str] = None,
    ) -> Optional[str]:
        from_dct_part_of = self.__get_catalog_name_by_dct_part_of(record_part_of_uri)
        if from_dct_part_of is not None:
            return from_dct_part_of
        else:
            try:
                catalog_idx = self.catalogs.index(dataset_node_uri)
                catalog = self.catalogs[catalog_idx]
                return catalog.name
            except (ValueError, AttributeError):
                return None

    def __get_catalog_name_by_dct_part_of(
        self: Any, record_part_of_uri: str
    ) -> Optional[str]:
        if record_part_of_uri is not None:
            try:
                catalog_idx = self.catalogs.index(record_part_of_uri)
                catalog = self.catalogs[catalog_idx]
                return catalog.name
            except (ValueError, AttributeError):
                return None
        else:
            return None

    def get_catalog_record_for_dataset(self: Any, dataset_uri: str) -> Optional[dict]:
        for record in self.catalog_records:
            if record.primary_topic_is(dataset_uri):
                return reduce_record(record.json_rdf_entry)
        return None

    def get_prefixed_formats_for_distributions(
        self: Any, dcat_distributions: List
    ) -> List[str]:
        distributions_formats: List[dict] = []
        for dist in dcat_distributions:
            distributions_formats = (
                distributions_formats
                + (dist.get(JsonRDF.dct.format) or [])
                + (dist.get(JsonRDF.dcat.mediaType) or [])
            )

        format_str_values = list(
            set(
                [
                    formats[ContentKeys.VALUE]
                    for formats in distributions_formats
                    if formats is not None
                ]
            )
        )
        return map_formats_to_prefixed(
            format_str_values, self.media_types_dict, self.file_types_dict
        )


def reduce_record(record: dict) -> dict:
    reduced_record = record[1].copy()
    for items in record[1].items():
        key = items[0]
        if key not in CATALOG_RECORD_AGGREGATION_FIELDS:
            reduced_record.pop(key)
    return reduced_record


def remove_nested_distributions(distribution: dict) -> dict:
    reduced_dict = distribution.copy()
    reduced_dict.pop(JsonRDF.dcat.distribution)
    return reduced_dict
