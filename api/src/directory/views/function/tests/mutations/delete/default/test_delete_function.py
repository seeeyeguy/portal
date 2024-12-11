"""
Collection of pytests for Function's delete view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "function",
    "views",
    "directory.function.delete",
    "function.delete.default",
    "views.TestDeleteFunction",
)
class TestDeleteFunction(TestCase):
    """
    Tests for DELETE /v1/directory/functions endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
    ]

    url: str = reverse("directory.function")

    @tag("views.function.delete_function")
    def test_delete_function(self) -> None:
        """Success Case: Delete a `Function` record."""
