"""
Collection of pytests for Function's fetch controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "function",
    "controllers.TestFetchFunction",
    "directory.function.fetch",
    "function.fetch.default",
)
class TestFetchFunction(TestCase):
    """Test suite for Function's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
    ]

    @tag("controllers.function.fetch_functions")
    def test_fetch_functions(self) -> None:
        """Success Case: Fetch all `Function` records."""

    @tag("controllers.function.fetch_function_by_id")
    def test_fetch_function_by_id(self) -> None:
        """Success Case: Fetch a `Function` record given an id."""

    @tag("controllers.function.fetch_function_by_id_dne")
    def test_fetch_function_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Function` record given an id where
        record does not exist."""
