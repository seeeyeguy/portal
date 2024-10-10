"""
Collection of pytests for Tag's search controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "tag",
    "controllers.TestSearchTag",
    "directory.tag.search",
    "tag.search.default",
)
class TestSearchTag(TestCase):
    """Test suite for Tag's search controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    @tag("controllers.tag.search_tags")
    def test_search_tags(self) -> None:
        """Success Case: Search for `Tag` records that match
        the given label."""
