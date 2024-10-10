"""
Collection of pytests for Tag's fetch view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "tag",
    "views",
    "directory.tag.fetch",
    "tag.fetch.default",
    "views.TestFetchTag",
)
class TestFetchTag(TestCase):
    """
    Tests for GET /v1/directory/tags endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    url: str = reverse("directory.tag")

    @tag("views.tag.fetch_tags")
    def test_fetch_tags(self) -> None:
        """Success Case: Fetch all `Tag` records."""

    @tag("views.tag.fetch_tags_with_page")
    def test_fetch_tags_with_page(self) -> None:
        """Success Case: Fetch page of `Tag` records."""

    @tag("views.tag.fetch_tags_with_limit")
    def test_fetch_tags_with_limit(self) -> None:
        """Success Case: Fetch all `Tag` records up to limit."""

    @tag("views.tag.fetch_tags_with_page_and_limit")
    def test_fetch_tags_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Tag` records up to limit."""

    @tag("views.tag.fetch_tag_by_id")
    def test_fetch_tag_by_id(self) -> None:
        """Success Case: Fetch a `Tag` record given an id."""

    @tag("views.tag.fetch_tag_by_id_dne")
    def test_fetch_tag_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Tag` record given an id where
        record does not exist."""
