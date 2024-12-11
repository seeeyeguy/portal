"""
Collection of pytests for Tag's delete view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "tag",
    "views",
    "directory.tag.delete",
    "tag.delete.default",
    "views.TestDeleteTag",
)
class TestDeleteTag(TestCase):
    """
    Tests for DELETE /v1/directory/tags endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    url: str = reverse("directory.tag")

    @tag("views.tag.delete_tag")
    def test_delete_tag(self) -> None:
        """Success Case: Delete a `Tag` record."""
