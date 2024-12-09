"""
Collection of pytests for Tag's update controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "tag",
    "controllers.TestUpdateTag",
    "directory.tag.update",
    "tag.update.default",
)
class TestUpdateTag(TestCase):
    """Test suite for Tag's update controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    @tag("controllers.tag.update_tag")
    def test_update_tag(self) -> None:
        """Success Case: Update a `Tag` record."""

    @tag("controllers.tag.update_tag_record_dne")
    def test_update_tag_record_dne(self) -> None:
        """Fail Case: Update a `Tag` that does not exist."""

    @tag("controllers.tag.update_tag_duplicate_label")
    def test_update_tag_duplicate_label(self) -> None:
        """Fail Case: Update a `Tag` record with a duplicate label."""

    @tag("controllers.tag.update_tag_empty_label")
    def test_update_tag_empty_label(self) -> None:
        """Fail Case: Update a `Tag` record with an empty label."""
