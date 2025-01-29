"""
Collection of pytests for Tag's delete controller.
"""

from typing import List

from django.test import tag, TestCase

from directory.controllers.Tag.Tag import Tag
from directory.controllers.Tag.tests.mutations.delete.default import arguments


@tag(
    "controllers",
    "directory",
    "tag",
    "controllers.TestDeleteTag",
    "directory.tag.delete",
    "tag.delete.default",
)
class TestDeleteTag(TestCase):
    """Test suite for Tag's delete controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    @tag("controllers.tag.delete_tag")
    def test_delete_tag(self) -> None:
        """Success Case: Delete a `Tag` record."""

        rows_affected = Tag.delete_tag(tag_id=arguments.DELETE_TAG_BY_ID)

        self.assertEqual(rows_affected, 1)
