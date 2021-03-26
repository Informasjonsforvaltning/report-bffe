import urllib.parse

import pytest

from src.sparql import (
    get_dataservice_publisher_query,
    get_dataservice_query,
    get_dataset_publisher_query,
)


@pytest.mark.unit
def test_dataset_publishers_query():
    publisher_query = urllib.parse.quote_plus(get_dataset_publisher_query().strip())
    assert publisher_query == (
        "PREFIX+dct%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0A++++++++"
        "PREFIX+dcat%3A+%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fdcat%23%3E%0A++++++++"
        "PREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0A++++++++"
        "PREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0A++++++++"
        "SELECT+DISTINCT+%3Fname+%3Fpublisher+%3FsameAs%0A++++++++"
        "FROM+%3Chttps%3A%2F%2Fdatasets.fellesdatakatalog.digdir.no%3E%0A++++++++"
        "WHERE+%7B%7B%0A++++++++++++%3Fsubject+dct%3Apublisher+%3Fpublisher+."
        "%0A++++++++++++%3Fpublisher+foaf%3Aname+%3Fname+.%0A++++++++++++"
        "OPTIONAL+%7B%7B%0A++++++++++++++++%3Fpublisher+owl%3AsameAs+%3FsameAs+."
        "%0A++++++++++++%7D%7D%0A++++++++%7D%7D"
    )


@pytest.mark.unit
def test_dataservice_query():
    dataservice_query = urllib.parse.quote_plus(get_dataservice_query().strip())
    assert dataservice_query == (
        "PREFIX+dct%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0A++++++++"
        "PREFIX+dcat%3A+%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fdcat%23%3E%0A++++++++"
        "PREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0A++++++++"
        "PREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0A++++++++"
        "SELECT+%3Frecord+%3Fpublisher+%3Fissued+%3FsameAs+%3FmediaType%0A++++++++"
        "FROM+%3Chttps%3A%2F%2Fdataservices.fellesdatakatalog.digdir.no%3E%0A++++++++"
        "WHERE+%7B%7B%0A++++++++++++%3Fcatalog+a+dcat%3ACatalog+.%0A++++++++++++%3Fcatalog+dct%3A"
        "publisher+%3Fpublisher+.%0A++++++++++++%3Fcatalog+dcat%3Aservice+%3Fservice+."
        "%0A++++++++++++%3Frecord+foaf%3AprimaryTopic+%3Fservice+."
        "%0A++++++++++++%3Frecord+dct%3Aissued+%3Fissued+.%0A++++++++++++"
        "OPTIONAL+%7B%7B%0A++++++++++++++++%3Fpublisher+owl%3AsameAs+%3FsameAs+."
        "%0A++++++++++++++++%3Fservice+dcat%3AmediaType+%3FmediaType+.%0A++++++++++++%7D%7D%0A++++++++%7D%7D"
    )


@pytest.mark.unit
def test_dataservice_publisher_query():
    dataservice_publisher_query = urllib.parse.quote_plus(
        get_dataservice_publisher_query().strip()
    )
    assert dataservice_publisher_query == (
        "PREFIX+dct%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0A++++++++"
        "PREFIX+dcat%3A+%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fdcat%23%3E%0A++++++++"
        "PREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0A++++++++"
        "SELECT+DISTINCT+%3Fpublisher+%3FsameAs%0A++++++++"
        "FROM+%3Chttps%3A%2F%2Fdataservices.fellesdatakatalog.digdir.no%3E%0A++++++++"
        "WHERE+%7B%7B%0A++++++++++++%3Fsubject+dct%3Apublisher+%3Fpublisher+.%0A++++++++++++"
        "OPTIONAL+%7B%7B%0A++++++++++++++++%3Fpublisher+owl%3AsameAs+%3FsameAs+.%0A++++++++++++%7D%7D%0A++++++++%7D%7D"
    )
