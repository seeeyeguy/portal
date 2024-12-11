"""
Collection of pytests for Tag's create view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "tag",
    "views",
    "directory.tag.create",
    "tag.create.default",
    "views.TestCreateTag",
)
class TestCreateTag(TestCase):
    """
    Tests for POST /v1/directory/tags endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    url: str = reverse("directory.tag")

    @tag("views.tag.create_tag")
    def test_create_tag(self) -> None:
        """Success Case: Create a `Tag` record."""

    @tag("views.tag.create_tag_duplicate_label")
    def test_create_tag_duplicate_label(self) -> None:
        """Fail Case: Create a `Tag` record with a duplicate label."""

    @tag("views.tag.create_tag_empty_label")
    def test_create_tag_empty_label(self) -> None:
        """Fail Case: Create a `Tag` record with an empty label."""
