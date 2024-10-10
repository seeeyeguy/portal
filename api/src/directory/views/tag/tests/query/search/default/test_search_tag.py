"""
Collection of pytests for Tag's search view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "tag",
    "views",
    "directory.tag.search",
    "tag.search.default",
    "views.TestSearchTag",
)
class TestSearchTag(TestCase):
    """
    Tests for GET /v1/directory/tags/search endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    url: str = reverse("directory.tag.search")

    @tag("views.tag.search_tags")
    def test_search_tags(self) -> None:
        """Success Case: Search for `Tag` records that match
        the given label."""
