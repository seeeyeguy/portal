"""
Collection of pytests for Tag's create controller.
"""

import pytest
from typing import List

from django.test import tag, TestCase

from directory.controllers import Tag
from directory.controllers.Tag.tests.mutations.create.default import arguments
from directory.exceptions import DirectoryError
from directory.models import Tag as TagModel
from directory.models.Tag.serializers import TagSerializer


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

        tag_record = Tag.create_tag(label=arguments.CREATE_TAG_LABEL)

        self.assertIsInstance(tag_record, TagModel)

        # Serialize `Tag`.
        serialized_tag = TagSerializer(tag_record).data

        del serialized_tag["created"]
        del serialized_tag["id"]
        del serialized_tag["modified"]

        self.assertEqual(serialized_tag, arguments.CREATE_TAG_EXPECTED_VALUE)

    @tag("controllers.tag.create_tag_duplicate_label")
    def test_create_tag_duplicate_label(self) -> None:
        """Fail Case: Create a `Tag` record with a duplicate label."""

        with pytest.raises(DirectoryError):
            _ = Tag.create_tag(label=arguments.CREATE_DUPLICATE_TAG)
