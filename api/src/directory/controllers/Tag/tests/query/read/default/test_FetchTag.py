"""
Collection of pytests for Tag's fetch controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import pytest
from typing import List

from django.db.models import QuerySet
from django.test import tag

from directory.controllers.Tag.Tag import Tag
from directory.controllers.Tag.tests.query.read.default import arguments
from directory.exceptions import DirectoryError
from directory.models.Tag.Tag import Tag as TagModel
from directory.models.Tag.serializers import TagSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "directory",
    "tag",
    "controllers.TestFetchTag",
    "directory.tag.fetch",
    "tag.fetch.default",
)
class TestFetchTag(MultiDBTestCase):
    """Test suite for Tag's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    @tag("controllers.tag.fetch_tags")
    def test_fetch_tags(self) -> None:
        """Success Case: Fetch all `Tag` records."""

        tags = Tag.fetch_tags()

        self.assertIsInstance(tags, QuerySet[TagModel])
        self.assertEqual(tags.count(), len(arguments.VALID_TAG_RECORDS.keys()))  # type: ignore[union-attr]

        for tag in tags:  # type: ignore[union-attr]
            self.assertIsInstance(tag, TagModel)

            tag_id: int = tag.id

            self.assertIn(tag_id, arguments.VALID_TAG_RECORDS)
            self.assertEqual(
                TagSerializer(tag).data, arguments.VALID_TAG_RECORDS[tag_id]
            )

    @tag("controllers.tag.fetch_tags_with_page")
    def test_fetch_tags_with_page(self) -> None:
        """Success Case: Fetch page of `Tag` records."""

        tags = Tag.fetch_tags(page=arguments.FETCH_TAG_WITH_PAGE)

        self.assertIsInstance(tags, QuerySet[TagModel])
        self.assertEqual(tags.count(), len(arguments.VALID_TAG_RECORDS.keys()))  # type: ignore[union-attr]

        for tag in tags:  # type: ignore[union-attr]
            self.assertIsInstance(tag, TagModel)

            tag_id: int = tag.id

            self.assertIn(tag_id, arguments.VALID_TAG_RECORDS)
            self.assertEqual(
                TagSerializer(tag).data, arguments.VALID_TAG_RECORDS[tag_id]
            )

    @tag("controllers.tag.fetch_tags_with_limit")
    def test_fetch_tags_with_limit(self) -> None:
        """Success Case: Fetch all `Tag` records up to limit."""

        tags = Tag.fetch_tags(limit=arguments.FETCH_TAG_WITH_LIMIT)

        self.assertIsInstance(tags, QuerySet[TagModel])
        self.assertEqual(tags.count(), len(arguments.FETCH_TAG_WITH_LIMIT_VALID_IDS))  # type: ignore[union-attr]

        for tag in tags:  # type: ignore[union-attr]
            self.assertIsInstance(tag, TagModel)

            tag_id: int = tag.id

            self.assertIn(tag_id, arguments.FETCH_TAG_WITH_LIMIT_VALID_IDS)
            self.assertEqual(
                TagSerializer(tag).data, arguments.VALID_TAG_RECORDS[tag_id]
            )

    @tag("controllers.tag.fetch_tags_with_page_and_limit")
    def test_fetch_tags_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Tag` records up to limit."""

        tags = Tag.fetch_tags(
            page=arguments.FETCH_TAG_WITH_PAGE,
            limit=arguments.FETCH_TAG_WITH_PAGE_AND_LIMIT_LIMIT_NUMBER,
        )

        self.assertIsInstance(tags, QuerySet[TagModel])
        self.assertEqual(tags.count(), len(arguments.FETCH_TAG_WITH_PAGE_AND_LIMIT_VALID_IDS))  # type: ignore[union-attr]

        for tag in tags:  # type: ignore[union-attr]
            self.assertIsInstance(tag, TagModel)

            tag_id: int = tag.id

            self.assertIn(tag_id, arguments.FETCH_TAG_WITH_PAGE_AND_LIMIT_VALID_IDS)
            self.assertEqual(
                TagSerializer(tag).data, arguments.VALID_TAG_RECORDS[tag_id]
            )

    @tag("controllers.tag.fetch_tags_with_page_exceeding_page_count")
    def test_fetch_tags_with_page_exceeding_page_count(self) -> None:
        """Success Case: Fetch page of `Tag` records using a
        page number that exceeds the number of pages."""

        tags = Tag.fetch_tags(page=arguments.FETCH_TAG_WITH_PAGE_EXCEEDING_PAGE_COUNT)

        self.assertIsInstance(tags, QuerySet[TagModel])
        self.assertEqual(
            tags.count(),  # type: ignore[union-attr]
            arguments.FETCH_TAG_WITH_PAGE_EXCEEDING_PAGE_COUNT_RECORD_COUNT,
        )

    @tag("controllers.tag.fetch_tag_by_id")
    def test_fetch_tag_by_id(self) -> None:
        """Success Case: Fetch a `Tag` record given an id."""

        tag = Tag.fetch_tags(tag_id=arguments.FETCH_TAG_BY_ID)

        self.assertIsInstance(tag, TagModel)

        tag_id: int = tag.id  # type: ignore[union-attr]

        self.assertIn(tag_id, arguments.VALID_TAG_RECORDS)
        self.assertEqual(TagSerializer(tag).data, arguments.VALID_TAG_RECORDS[tag_id])

    @tag("controllers.tag.fetch_tag_by_id_dne")
    def test_fetch_tag_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Tag` record given an id where
        record does not exist."""

        with pytest.raises(DirectoryError):
            _ = Tag.fetch_tags(tag_id=arguments.FETCH_TAG_BY_ID_DNE)

    @tag("controllers.tag.fetch_tag_by_id_with_page")
    def test_fetch_tag_by_id_with_page(self) -> None:
        """Fail Case: Fetch a `Tag` record given an id where
        a page is also supplied in the parameters."""

        with pytest.raises(DirectoryError):
            _ = Tag.fetch_tags(
                tag_id=arguments.FETCH_TAG_BY_ID, page=arguments.FETCH_TAG_WITH_PAGE
            )

    @tag("controllers.tag.fetch_tag_by_id_with_limit")
    def test_fetch_tag_by_id_with_limit(self) -> None:
        """Fail Case: Fetch a `Tag` record given an id where
        a limit is also supplied in the parameters."""

        with pytest.raises(DirectoryError):
            _ = Tag.fetch_tags(
                tag_id=arguments.FETCH_TAG_BY_ID, limit=arguments.FETCH_TAG_WITH_LIMIT
            )

    @tag("controllers.tag.fetch_tag_by_id_with_page_and_limit")
    def test_fetch_tag_by_id_with_page_and_limit(self) -> None:
        """Fail Case: Fetch a `Tag` record given an id where
        a page and limit is also supplied in the parameters."""

        with pytest.raises(DirectoryError):
            _ = Tag.fetch_tags(
                tag_id=arguments.FETCH_TAG_BY_ID,
                page=arguments.FETCH_TAG_WITH_PAGE,
                limit=arguments.FETCH_TAG_WITH_LIMIT,
            )
