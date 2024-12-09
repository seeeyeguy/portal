"""
Collection of pytests for Function's create view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "function",
    "views",
    "directory.function.create",
    "function.create.default",
    "views.TestCreateFunction",
)
class TestCreateFunction(TestCase):
    """
    Tests for POST /v1/directory/functions endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
    ]

    url: str = reverse("directory.function")

    @tag("views.function.create_function")
    def test_create_function(self) -> None:
        """Success Case: Create a `Function` record."""

    @tag("views.function.create_function_duplicate_name")
    def test_create_function_duplicate_name(self) -> None:
        """Fail Case: Create a `Function` record with a duplicate name."""
