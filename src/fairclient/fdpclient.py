# SPDX-FileCopyrightText: 2024 Stichting Health-RI
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import logging
from enum import Enum
from urllib.parse import urlparse

import requests
from rdflib import Graph, URIRef

from fairclient.basicclient import BasicAPIClient

logger = logging.getLogger(__name__)


class FDPEndPoints(Enum):
    meta = "meta"
    state = f"{meta}/state"
    members = "members"
    expanded = "expanded"

    def __str__(self):
        return str(self.value)


class FDPClient(BasicAPIClient):
    """Client for FAIR Data Point client"""

    def __init__(self, base_url: str, username: str, password: str):
        """Initializes an FDP Client object

        Parameters
        ----------
        base_url : str
            Base URL of the Fair Data Point
        username : str
            username for authentication
        password : str
            password for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.username = username
        # Don't store password for security reasons (might show up in a stack trace or something)
        # self.password = password
        logger.debug("Logging into FDP %s with user %s", self.base_url, self.username)
        self.__token = self.login_fdp(username, password)
        headers = self.get_headers()
        super().__init__(self.base_url, headers)

    def login_fdp(self, username: str, password: str, timeout: float = 60) -> str:
        """Logs in to a Fair Data Point and retrieves a JWT token

        Parameters
        ----------
        username : str
            username for authentication
        password : str
            password for authentication
        timeout : float, optional
            timeout for login request, by default 60

        Returns
        -------
        str
            JWT authentication token
        """
        token_response = requests.post(
            f"{self.base_url}/tokens",
            json={"email": username, "password": password},
            timeout=timeout,
        )
        token_response.raise_for_status()
        response = token_response.json()
        token = response["token"]
        self.__token = token
        return token

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.__token}",
            "Content-Type": "text/turtle",
        }

    def _update_session_headers(self):
        self.session.headers.update(self.headers)

    def _change_content_type(self, content_type: str):
        self.headers["Content-Type"] = content_type
        self._update_session_headers()

    def post_serialized(self, resource_type: str, metadata: Graph) -> requests.Response:
        """Serializes and POSTs a graph to an FDP

        Parameters
        ----------
        resource_type : str
            Type of resource to push (e.g. 'dataset')
        metadata : Graph
            The graph with metadata to be pusshed

        Returns
        -------
        requests.Response
            The response from the FDP
        """
        self._change_content_type("text/turtle")
        path = f"{self.base_url}/{resource_type}"
        logger.debug("Posting metadata to %s", path)
        return self.post(path=path, data=metadata.serialize(format="turtle"))

    def update_serialized(self, resource_uri: str, metadata: Graph) -> requests.Response:
        """Serializes and updates (PUTs) a graph on an FDP

        Parameters
        ----------
        resource_uri : str
            URI to update
        metadata : Graph
            The graph with metadata to be pusshed

        Returns
        -------
        requests.Response
            The response from the FDP
        """
        self._change_content_type("text/turtle")
        request_url = self._to_request_url(resource_uri)
        logger.debug("Putting metadata to %s", request_url)
        return self.update(path=request_url, data=metadata.serialize(format="turtle"))

    def get_data(self, path: str) -> requests.Response:
        return self.get(path=self._to_request_url(path))

    def delete_record(self, path: str) -> requests.Response:
        return self.delete(path=self._to_request_url(path))

    def _to_request_url(self, resource_uri: str) -> str:
        """Re-anchors a resource URI onto the base URL of this client

        From FDP 1.17 onwards the identifiers an FDP hands out are derived from its
        configured persistent URL rather than from the URL it is reached on. This applies
        to the ``Location`` header of a POST, but equally to the subjects returned by a
        SPARQL query of the triplestore. Behind a reverse proxy such an identifier may use
        a different scheme, host or port than the one used to reach the FDP, and is then
        not connectable. Only the path is reused; the base URL of this client is
        authoritative for where requests are sent.

        Relative paths are passed through, so this is safe to apply to any argument that
        may be either a full record URI or a path relative to the base URL.

        Parameters
        ----------
        resource_uri : str
            URI of a record (e.g. a ``Location`` header or a SPARQL subject), or a path
            relative to the base URL of this client

        Returns
        -------
        str
            URL pointing at the same record on the host this client talks to
        """
        parsed = urlparse(str(resource_uri))
        if not parsed.scheme and not parsed.netloc:
            # A relative path, urljoin in the underlying client resolves this correctly
            return str(resource_uri)

        request_url = f"{self.base_url}{parsed.path}"
        if request_url != str(resource_uri):
            logger.debug("Rewrote resource URI %s to %s", resource_uri, request_url)
        return request_url

    def publish_record(self, record_url: str):
        """Changes the status of an FDP record to "Published"

        Parameters
        ----------
        record_url : str
            URL of the record that is to be published
        """
        self._change_content_type("application/json")
        path = f"{self._to_request_url(record_url)}/{FDPEndPoints.state}"
        data = '{"current": "PUBLISHED"}'
        self.update(path=path, data=data)

    def create_and_publish(self, resource_type: str, metadata: Graph) -> URIRef:
        """Creates and publishes a record in the FDP

        Parameters
        ----------
        resource_type : str
            Type of record to publish (e.g. Catalog, Distribution, Dataset)
        metadata : Graph
            The metadata to be published

        Returns
        -------
        URIRef
            URI of (subject of) published dataset
        """
        post_response = self.post_serialized(resource_type=resource_type, metadata=metadata)

        # FDP will return a 201 status code with the new identifier of the published record
        fdp_subject = URIRef(post_response.headers["Location"])

        # Change status to 'published' so that metadata shows in catalog
        logger.debug("New FDP subject: %s", fdp_subject)
        self.publish_record(fdp_subject)

        return fdp_subject
