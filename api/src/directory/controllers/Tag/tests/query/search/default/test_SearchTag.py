"""
Collection of pytests for Tag's search controller.
"""

from typing import List

from django.db.models import QuerySet
from django.test import tag

from directory import controllers, models
from directory.controllers.Tag.tests.query.search.default import arguments
from directory.models.Tag.serializers import TagSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "directory",
    "tag",
    "controllers.TestSearchTag",
    "directory.tag.search",
    "tag.search.default",
)
class TestSearchTag(MultiDBTestCase):
    """Test suite for Tag's search controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    @tag("controllers.tag.search_tags")
    def test_search_tags(self) -> None:
        """Success Case: Search for `Tag` records that match
        the given label."""

        # Call search controller.
        search_results: QuerySet[models.Tag] = controllers.Tag.search_tags(
            arguments.SEARCH_TERM
        )

        # Ensure two `Tag`s are returned.
        self.assertEqual(len(search_results), 2)

        # Ensure each `Tag` label starts with the search term.
        for result in search_results:
            self.assertIsInstance(result, models.Tag)
            self.assertTrue(result.label.startswith(arguments.SEARCH_TERM))
            serialized_tag = TagSerializer(result).data
            self.assertEqual(serialized_tag, arguments.EXPECTED_TAG_RECORDS[result.id])

    @tag("controllers.tag.search_tags_no_results")
    def test_search_tags_no_results(self) -> None:
        """Success Case: Search for `Tag` records that match
        the given label but none exist."""

        # Call search controller.
        search_results: QuerySet[models.Tag] = controllers.Tag.search_tags(
            arguments.SEARCH_TERM_NO_RESULTS
        )

        # Ensure an empty QuerySet is returned.
        self.assertEqual(len(search_results), 0)
