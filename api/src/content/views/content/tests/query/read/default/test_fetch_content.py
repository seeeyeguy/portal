"""
Collection of pytests for Content's fetch view endpoint.
"""

from typing import List

from django.test import tag
from django.urls import reverse
from rest_framework import status

from content.controllers.Content.tests.query.read.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "content",
    "views",
    "content.content.fetch",
    "resource.fetch.default",
    "views.TestFetchContent",
)
class TestFetchContent(MultiDBTestCase):
    """
    Tests for GET /v1/content/content endpoint.
    """

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "content/controllers/Content/tests/query/read/default/fixtures/content.json",
    ]

    url: str = reverse("content.content")

    @tag("views.content.fetch_content")
    def test_fetch_content(self) -> None:
        """Success Case: Fetch a `Content` record."""

        url: str = f"{self.url}?key={arguments.FETCH_CONTENT_CONTENT_KEY}"
        response = self.client.get(url, headers={"content_type": "application/json"})

        content = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(content, dict)

        self.assertEqual(content, arguments.EXPECTED_CONTENT_RECORD)

    @tag("views.content.fetch_content_dne")
    def test_fetch_content_dne(self) -> None:
        """Fail Case: Fetch a `Content` record that
        does not exist."""

        url: str = f"{self.url}?key={arguments.FETCH_CONTENT_CONTENT_KEY_DNE}"
        response = self.client.get(url, headers={"content_type": "application/json"})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
