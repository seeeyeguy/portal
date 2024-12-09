"""
Collection of pytests for Tag's create controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "tag",
    "controllers.TestCreateTag",
    "directory.tag.create",
    "tag.create.default",
)
class TestCreateTag(TestCase):
    """Test suite for Tag's create controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    @tag("controllers.tag.create_tag")
    def test_create_tag(self) -> None:
        """Success Case: Create a `Tag` record."""

    @tag("controllers.tag.create_tag_duplicate_label")
    def test_create_tag_duplicate_label(self) -> None:
        """Fail Case: Create a `Tag` record with a duplicate label."""

    @tag("controllers.tag.create_tag_empty_label")
    def test_create_tag_empty_label(self) -> None:
        """Fail Case: Create a `Tag` record with an empty label."""
