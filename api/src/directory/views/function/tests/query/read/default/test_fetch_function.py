"""
Collection of pytests for Function's fetch view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from directory.controllers.Function.tests.query.read.default import arguments


@tag(
    "directory",
    "function",
    "views",
    "directory.function.fetch",
    "function.fetch.default",
    "views.TestFetchFunction",
)
class TestFetchFunction(TestCase):
    """
    Tests for GET /v1/directory/functions endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
    ]

    url: str = reverse("directory.function")

    @tag("views.function.fetch_functions")
    def test_fetch_functions(self) -> None:
        """Success Case: Fetch all `Function` records."""

        response = self.client.get(
            self.url, headers={"content-type": "application/json"}
        )

        functions = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(functions, List)
        self.assertCountEqual(
            functions, list(arguments.VALID_FUNCTION_RECORDS.values())
        )

    @tag("views.function.fetch_function_by_id")
    def test_fetch_function_by_id(self) -> None:
        """Success Case: Fetch a `Function` record given an id."""

        request_url: str = f"{self.url}?id={arguments.FETCH_FUNCTION_BY_ID}"
        response = self.client.get(
            request_url, headers={"content-type": "application/json"}
        )

        function = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(function, dict)
        self.assertEqual(
            function,
            arguments.VALID_FUNCTION_RECORDS[arguments.FETCH_FUNCTION_BY_ID],
        )

    @tag("views.function.fetch_function_by_id_dne")
    def test_fetch_function_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Function` record given an id where
        record does not exist."""

        request_url: str = f"{self.url}?id={arguments.FETCH_FUNCTION_BY_ID_DNE}"
        response = self.client.get(
            request_url, headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
