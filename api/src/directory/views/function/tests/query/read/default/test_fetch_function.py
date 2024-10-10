"""
Collection of pytests for Function's fetch view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


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

    @tag("views.function.fetch_function_by_id")
    def test_fetch_function_by_id(self) -> None:
        """Success Case: Fetch a `Function` record given an id."""

    @tag("views.function.fetch_function_by_id_dne")
    def test_fetch_function_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Function` record given an id where
        record does not exist."""
