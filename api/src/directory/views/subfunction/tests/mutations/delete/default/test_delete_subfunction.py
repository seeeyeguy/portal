"""
Collection of pytests for SubFunction's delete view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "subfunction",
    "views",
    "directory.subfunction.delete",
    "subfunction.delete.default",
    "views.TestDeleteSubFunction",
)
class TestDeleteSubFunction(TestCase):
    """
    Tests for DELETE /v1/directory/subfunctions endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    url: str = reverse("directory.subfunction")

    @tag("views.subfunction.delete_subfunction")
    def test_delete_subfunction(self) -> None:
        """Success Case: Delete a `SubFunction` record."""
