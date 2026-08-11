#!/usr/bin/env python3
"""Upload test data to the dev FAIR Data Point.

Pushes a catalog and a dataset, linked to that catalog, to the dev FDP.

Usage:
    python dev-setup/fdp/upload_data.py
"""

from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

import requests
from fairclient.fdpclient import FDPClient
from rdflib import DCAT, DCTERMS, RDF, Graph, URIRef

logger = logging.getLogger(__name__)

FDP_URL = "http://fdp.test"
FDP_USER = "albert.einstein@example.com"
FDP_PASSWORD = "password"

DATA_DIR = Path(__file__).parent / "data"
CATALOG_TTL = DATA_DIR / "test-catalog.ttl"
DATASET_TTL = DATA_DIR / "test-dataset.ttl"

WAIT_TIMEOUT_SECONDS = 300
WAIT_INTERVAL_SECONDS = 5


def wait_for_fdp(url: str) -> None:
    """Blocks until the FDP answers, so the upload does not race its startup."""
    deadline = time.monotonic() + WAIT_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        try:
            requests.get(url, timeout=WAIT_INTERVAL_SECONDS).raise_for_status()
        except requests.RequestException:
            logger.info("Waiting for %s ...", url)
            time.sleep(WAIT_INTERVAL_SECONDS)
        else:
            return
    msg = f"{url} did not become available within {WAIT_TIMEOUT_SECONDS} seconds"
    raise TimeoutError(msg)


def load_graph(path: Path) -> Graph:
    if not path.is_file():
        msg = f"Template not found at {path}"
        raise FileNotFoundError(msg)
    return Graph().parse(path, format="turtle")


def link_to_catalog(dataset: Graph, catalog_uri: URIRef) -> Graph:
    """Points the dct:isPartOf of every dcat:Dataset at the created catalog.

    This replaces the __CATALOG_UUID__ placeholder that test-dataset.ttl ships with.
    """
    subjects = list(dataset.subjects(RDF.type, DCAT.Dataset, unique=True))
    if not subjects:
        msg = "No dcat:Dataset subject found in the dataset graph"
        raise ValueError(msg)
    for subject in subjects:
        dataset.remove((subject, DCTERMS.isPartOf, None))
        dataset.add((subject, DCTERMS.isPartOf, catalog_uri))
    return dataset


def upload(fdp_url: str, catalog_ttl: Path, dataset_ttl: Path) -> None:
    """Creates and publishes a catalog and a linked dataset on the FDP."""
    catalog_graph = load_graph(catalog_ttl)
    dataset_graph = load_graph(dataset_ttl)

    client = FDPClient(fdp_url, FDP_USER, FDP_PASSWORD)

    catalog_uri = client.create_and_publish("catalog", catalog_graph)
    logger.info("%s: created and published catalog %s", fdp_url, catalog_uri)

    link_to_catalog(dataset_graph, catalog_uri)
    dataset_uri = client.create_and_publish("dataset", dataset_graph)
    logger.info("%s: created and published dataset %s", fdp_url, dataset_uri)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    wait_for_fdp(FDP_URL)
    upload(FDP_URL, CATALOG_TTL, DATASET_TTL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
