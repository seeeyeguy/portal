"""
Collection of pytests for SubFunction's fetch view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from directory.controllers.SubFunction.tests.query.read.default import arguments


@tag(
    "directory",
    "subfunction",
    "views",
    "directory.subfunction.fetch",
    "subfunction.fetch.default",
    "views.TestFetchSubFunction",
)
class TestFetchSubFunction(TestCase):
    """
    Tests for GET /v1/directory/subfunctions endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    url: str = reverse("directory.subfunction")

    @tag("views.subfunction.fetch_subfunctions")
    def test_fetch_subfunctions(self) -> None:
        """Success Case: Fetch all `SubFunction` records."""

        response = self.client.get(
            self.url, headers={"content-type": "application/json"}
        )

        subfunctions = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(subfunctions, List)
        self.assertCountEqual(
            subfunctions, list(arguments.VALID_SUBFUNCTION_RECORDS.values())
        )

    @tag("views.subfunction.fetch_subfunction_by_id")
    def test_fetch_subfunction_by_id(self) -> None:
        """Success Case: Fetch a `SubFunction` record given an id."""

        request_url: str = f"{self.url}?id={arguments.FETCH_SUBFUNCTION_BY_ID}"
        response = self.client.get(
            request_url, headers={"content-type": "application/json"}
        )

        subfunction = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(subfunction, dict)
        self.assertEqual(
            subfunction,
            arguments.VALID_SUBFUNCTION_RECORDS[arguments.FETCH_SUBFUNCTION_BY_ID],
        )

    @tag("views.subfunction.fetch_subfunction_by_id_dne")
    def test_fetch_subfunction_by_id_dne(self) -> None:
        """Fail Case: Fetch a `SubFunction` record given an id where
        record does not exist."""

        request_url: str = f"{self.url}?id={arguments.FETCH_SUBFUNCTION_BY_ID_DNE}"
        response = self.client.get(
            request_url, headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
