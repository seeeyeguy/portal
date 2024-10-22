"""
Collection of pytests for Tag's fetch view endpoint.
"""

# pylint: disable=line-too-long
from typing import List

from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from directory.controllers.Tag.tests.query.read.default import arguments


@tag(
    "directory",
    "tag",
    "views",
    "directory.tag.fetch",
    "tag.fetch.default",
    "views.TestFetchTag",
)
class TestFetchTag(TestCase):
    """
    Tests for GET /v1/directory/tags endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
    ]

    url: str = reverse("directory.tag")

    @tag("views.tag.fetch_tags")
    def test_fetch_tags(self) -> None:
        """Success Case: Fetch all `Tag` records."""

        response = self.client.get(self.url)

        tags = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(tags, List)
        self.assertEqual(len(tags), len(arguments.VALID_TAG_RECORDS))

        for tag in tags:
            self.assertIsInstance(tag, dict)

            tag_id: int = tag["id"]

            self.assertIn(tag_id, arguments.VALID_TAG_RECORDS)
            self.assertEqual(tag, arguments.VALID_TAG_RECORDS[tag_id])

    @tag("views.tag.fetch_tags_with_page")
    def test_fetch_tags_with_page(self) -> None:
        """Success Case: Fetch page of `Tag` records."""

        request_url: str = f"{self.url}?page={arguments.FETCH_TAG_WITH_PAGE}"
        response = self.client.get(request_url)

        tags = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(tags, List)
        self.assertEqual(len(tags), len(arguments.VALID_TAG_RECORDS))

        for tag in tags:
            self.assertIsInstance(tag, dict)

            tag_id: int = tag["id"]

            self.assertIn(tag_id, arguments.VALID_TAG_RECORDS)
            self.assertEqual(tag, arguments.VALID_TAG_RECORDS[tag_id])

    @tag("views.tag.fetch_tags_with_limit")
    def test_fetch_tags_with_limit(self) -> None:
        """Success Case: Fetch all `Tag` records up to limit."""

        request_url: str = f"{self.url}?limit={arguments.FETCH_TAG_WITH_LIMIT}"
        response = self.client.get(request_url)

        tags = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(tags, List)
        self.assertEqual(len(tags), len(arguments.FETCH_TAG_WITH_LIMIT_VALID_IDS))

        for tag in tags:
            self.assertIsInstance(tag, dict)

            tag_id: int = tag["id"]

            self.assertIn(tag_id, arguments.FETCH_TAG_WITH_LIMIT_VALID_IDS)
            self.assertEqual(tag, arguments.VALID_TAG_RECORDS[tag_id])

    @tag("views.tag.fetch_tags_with_page_and_limit")
    def test_fetch_tags_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Tag` records up to limit."""

        request_url: str = f"{self.url}?page={arguments.FETCH_TAG_WITH_PAGE}&limit={arguments.FETCH_TAG_WITH_PAGE_AND_LIMIT_LIMIT_NUMBER}"
        response = self.client.get(request_url)

        tags = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(tags, List)
        self.assertEqual(
            len(tags), len(arguments.FETCH_TAG_WITH_PAGE_AND_LIMIT_VALID_IDS)
        )

        for tag in tags:
            self.assertIsInstance(tag, dict)

            tag_id: int = tag["id"]

            self.assertIn(tag_id, arguments.FETCH_TAG_WITH_PAGE_AND_LIMIT_VALID_IDS)
            self.assertEqual(tag, arguments.VALID_TAG_RECORDS[tag_id])

    @tag("views.tag.fetch_tags_with_page_exceeding_page_count")
    def test_fetch_tags_with_page_exceeding_page_count(self) -> None:
        """Success Case: Fetch page of `Tag` records using a
        page number that exceeds the number of pages."""

        request_url: str = (
            f"{self.url}?page={arguments.FETCH_TAG_WITH_PAGE_EXCEEDING_PAGE_COUNT}"
        )
        response = self.client.get(request_url)

        tags = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(tags, List)
        self.assertEqual(
            len(tags), arguments.FETCH_TAG_WITH_PAGE_EXCEEDING_PAGE_COUNT_RECORD_COUNT
        )

    @tag("views.tag.fetch_tag_by_id")
    def test_fetch_tag_by_id(self) -> None:
        """Success Case: Fetch a `Tag` record given an id."""

        request_url: str = f"{self.url}?id={arguments.FETCH_TAG_BY_ID}"
        response = self.client.get(request_url)

        tag = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(tag, dict)

        tag_id: int = tag["id"]

        self.assertIn(tag_id, arguments.VALID_TAG_RECORDS)
        self.assertEqual(tag, arguments.VALID_TAG_RECORDS[tag_id])

    @tag("views.tag.fetch_tag_by_id_dne")
    def test_fetch_tag_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Tag` record given an id where
        record does not exist."""

        request_url: str = f"{self.url}?id={arguments.FETCH_TAG_BY_ID_DNE}"
        response = self.client.get(request_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.tag.fetch_tag_by_id_with_page")
    def test_fetch_tag_by_id_with_page(self) -> None:
        """Fail Case: Fetch a `Tag` record given an id where
        a page is also supplied in the parameters."""

        request_url: str = f"{self.url}?id={arguments.FETCH_TAG_BY_ID_DNE}&page={arguments.FETCH_TAG_WITH_PAGE}"
        response = self.client.get(request_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.tag.fetch_tag_by_id_with_limit")
    def test_fetch_tag_by_id_with_limit(self) -> None:
        """Fail Case: Fetch a `Tag` record given an id where
        a limit is also supplied in the parameters."""

        request_url: str = f"{self.url}?id={arguments.FETCH_TAG_BY_ID_DNE}&limit={arguments.FETCH_TAG_WITH_LIMIT}"
        response = self.client.get(request_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.tag.fetch_tag_by_id_with_page_and_limit")
    def test_fetch_tag_by_id_with_page_and_limit(self) -> None:
        """Fail Case: Fetch a `Tag` record given an id where
        a page and limit is also supplied in the parameters."""

        request_url: str = f"{self.url}?id={arguments.FETCH_TAG_BY_ID_DNE}&page={arguments.FETCH_TAG_WITH_PAGE}&limit={arguments.FETCH_TAG_WITH_LIMIT}"
        response = self.client.get(request_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
