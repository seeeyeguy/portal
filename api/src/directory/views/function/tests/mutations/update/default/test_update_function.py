"""
Collection of pytests for Function's update view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "function",
    "views",
    "directory.function.update",
    "function.update.default",
    "views.TestUpdateFunction",
)
class TestUpdateFunction(TestCase):
    """
    Tests for PUT /v1/directory/functions endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
    ]

    url: str = reverse("directory.function")

    @tag("views.function.update_function")
    def test_update_function(self) -> None:
        """Success Case: Update a `Function` record."""

    @tag("views.function.update_function_record_dne")
    def test_update_function_record_dne(self) -> None:
        """Fail Case: Update a `Function` that does not exist."""

    @tag("views.function.update_function_duplicate_name")
    def test_update_function_duplicate_name(self) -> None:
        """Fail Case: Update a `Function` record with a duplicate name."""
