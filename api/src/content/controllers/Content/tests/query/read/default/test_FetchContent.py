"""
Collection of pytests for Content's fetch controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import pytest
from typing import List

from django.test import tag

from content.controllers.Content.Content import Content
from content.controllers.Content.tests.query.read.default import arguments
from content.exceptions import ContentError
from content.models.Content.Content import Content as ContentModel
from content.models.Content.serializers import ContentSerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "content",
    "controllers.TestFetchContent",
    "content.content.fetch",
    "content.fetch.default",
)
class TestFetchContent(MultiDBTestCase):
    """Test Suite for Content's fetch controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "content/controllers/Content/tests/query/read/default/fixtures/content.json",
    ]

    @tag("controllers.content.fetch_content")
    def test_fetch_content(self) -> None:
        """Success Case: Fetch a `Content` record."""

        content = Content.fetch_content(key=arguments.FETCH_CONTENT_CONTENT_KEY)
        self.assertIsInstance(content, ContentModel)
        data = ContentSerializer(content).data
        self.assertEqual(data, arguments.EXPECTED_CONTENT_RECORD)

    @tag("controllers.content.fetch_content_dne")
    def test_fetch_content_dne(self) -> None:
        """Fail Case: Fetch a `Content` record that
        does not exist."""

        with pytest.raises(ContentError):
            _ = Content.fetch_content(key=arguments.FETCH_CONTENT_CONTENT_KEY_DNE)
