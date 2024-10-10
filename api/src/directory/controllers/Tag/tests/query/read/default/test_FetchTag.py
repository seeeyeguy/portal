"""
Collection of pytests for Tag's fetch controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "tag",
    "controllers.TestFetchTag",
    "directory.tag.fetch",
    "tag.fetch.default",
)
class TestFetchTag(TestCase):
    """Test suite for Tag's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    @tag("controllers.tag.fetch_tags")
    def test_fetch_tags(self) -> None:
        """Success Case: Fetch all `Tag` records."""

    @tag("controllers.tag.fetch_tags_with_page")
    def test_fetch_tags_with_page(self) -> None:
        """Success Case: Fetch page of `Tag` records."""

    @tag("controllers.tag.fetch_tags_with_limit")
    def test_fetch_tags_with_limit(self) -> None:
        """Success Case: Fetch all `Tag` records up to limit."""

    @tag("controllers.tag.fetch_tags_with_page_and_limit")
    def test_fetch_tags_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Tag` records up to limit."""

    @tag("controllers.tag.fetch_tag_by_id")
    def test_fetch_tag_by_id(self) -> None:
        """Success Case: Fetch a `Tag` record given an id."""

    @tag("controllers.tag.fetch_tag_by_id_dne")
    def test_fetch_tag_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Tag` record given an id where
        record does not exist."""
