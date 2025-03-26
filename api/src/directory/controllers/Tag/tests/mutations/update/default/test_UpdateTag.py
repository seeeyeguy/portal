"""
Collection of pytests for Tag's update controller.
"""

import pytest
from typing import List

from django.test import tag

from directory.controllers import Tag
from directory.controllers.Tag.tests.mutations.update.default import arguments
from directory.exceptions import DirectoryError
from directory.models.Tag import Tag as TagModel
from directory.models.Tag.serializers import TagSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "directory",
    "tag",
    "controllers.TestUpdateTag",
    "directory.tag.update",
    "tag.update.default",
)
class TestUpdateTag(MultiDBTestCase):
    """Test suite for Tag's update controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    @tag("controllers.tag.update_tag")
    def test_update_tag(self) -> None:
        """Success Case: Update a `Tag` record."""

        # Update `Tag` record.
        tag_record, rows_affected = Tag.update_tag(
            tag_id=arguments.UPDATE_TAG_ID, label=arguments.UPDATE_TAG_LABEL
        )

        self.assertIsInstance(tag_record, TagModel)

        # Serialize `Tag`.
        serialized_tag = TagSerializer(tag_record).data

        # Remove dynamic datetime fields before comparison.
        del serialized_tag["created"]
        del serialized_tag["modified"]

        self.assertEqual(rows_affected, 1)
        self.assertEqual(serialized_tag, arguments.UPDATE_TAG_EXPECTED_VALUES)

    @tag("controllers.tag.update_tag_record_dne")
    def test_update_tag_record_dne(self) -> None:
        """Fail Case: Update a `Tag` that does not exist."""

        with pytest.raises(DirectoryError):
            _, __ = Tag.update_tag(
                tag_id=arguments.UPDATE_TAG_ID_DNE, label=arguments.UPDATE_TAG_LABEL
            )

    @tag("controllers.tag.update_tag_duplicate_label")
    def test_update_tag_duplicate_label(self) -> None:
        """Fail Case: Update a `Tag` record with a duplicate label."""

        with pytest.raises(DirectoryError):
            _, __ = Tag.update_tag(
                tag_id=arguments.UPDATE_TAG_ID,
                label=arguments.UPDATE_TAG_LABEL_DUPLICATE,
            )
