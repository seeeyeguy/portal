"""
Collection of pytests for Tag's update view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "tag",
    "views",
    "directory.tag.update",
    "tag.update.default",
    "views.TestUpdateTag",
)
class TestUpdateTag(TestCase):
    """
    Tests for PUT /v1/directory/tags endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    url: str = reverse("directory.tag")

    @tag("views.tag.update_tag")
    def test_update_tag(self) -> None:
        """Success Case: Update a `Tag` record."""

    @tag("views.tag.update_tag_record_dne")
    def test_update_tag_record_dne(self) -> None:
        """Fail Case: Update a `Tag` that does not exist."""

    @tag("views.tag.update_tag_duplicate_label")
    def test_update_tag_duplicate_label(self) -> None:
        """Fail Case: Update a `Tag` record with a duplicate label."""

    @tag("views.tag.update_tag_empty_label")
    def test_update_tag_empty_label(self) -> None:
        """Fail Case: Update a `Tag` record with an empty label."""
