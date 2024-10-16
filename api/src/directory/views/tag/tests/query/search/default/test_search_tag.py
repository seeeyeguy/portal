"""
Collection of pytests for Tag's search view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from directory.controllers.Tag.tests.query.search.default import arguments


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

        # Make request to search `Tag`s endpoint.
        request_url = f"{self.url}?label={arguments.SEARCH_TERM}"
        response = self.client.get(request_url)
        tags = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure two serialized `Tag`s are returned.
        self.assertEqual(len(tags), 2)

        # Ensure each serialized `Tag` label starts with the search term.
        for record in tags:
            self.assertEqual(record, arguments.EXPECTED_TAG_RECORDS[record["id"]])
            self.assertTrue(record["label"].startswith(arguments.SEARCH_TERM))

    @tag("views.tag.search_tags_no_results")
    def test_search_tags_no_results(self) -> None:
        """Success Case: Search for `Tag` records that match
        the given label but none exist."""

        # Make request to search `Tag`s endpoint.
        request_url = f"{self.url}?label={arguments.SEARCH_TERM_NO_RESULTS}"
        response = self.client.get(request_url)
        tags = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure an empty list is returned.
        self.assertEqual(len(tags), 0)
