"""
Collection of pytests for Content's create controller.
"""

from typing import List

import pytest

from django.contrib.auth import models as AuthModels
from django.test import tag

from content import controllers
from content.controllers.Content.tests.mutations.create.default import arguments
from content.exceptions import ContentError
from content.models.Content.serializers import ContentSerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "content",
    "controllers.TestCreateContent",
    "content.content.create",
    "content.create.default",
)
class TestCreateContent(MultiDBTestCase):
    """Test suite for Content's create controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "content/controllers/Content/tests/mutations/create/default/fixtures/users.json",
    ]

    @tag("controllers.content.create_content")
    def test_create_content(self) -> None:
        """Success Case: Create a `Content` record."""

        created_by = AuthModels.User.objects.get(
            username=arguments.CREATE_CONTENT_CONTENT_CREATED_BY
        )
        record = controllers.Content.create_content(
            key=arguments.CREATE_CONTENT_CONTENT_KEY,
            content=arguments.CREATE_CONTENT_CONTENT_CONTENT,
            created_by=created_by,
        )

        data = ContentSerializer(record).data

        self.assertEqual(data["key"], arguments.CREATE_CONTENT_CONTENT_KEY)
        self.assertEqual(data["content"], arguments.CREATE_CONTENT_CONTENT_CONTENT)
        self.assertEqual(
            data["modified_by"], arguments.CREATE_CONTENT_CONTENT_CREATED_BY
        )

    @tag("controllers.content.create_content_not_authorized")
    def test_create_content_not_authorized(self) -> None:
        """Fail Case: Create a `Content` record with a user
        without proper permissions."""

        with pytest.raises(ContentError):
            created_by = AuthModels.User.objects.get(
                username=arguments.CREATE_CONTENT_CONTENT_CREATED_BY_NOT_AUTHORIZED
            )
            _ = controllers.Content.create_content(
                key=arguments.CREATE_CONTENT_CONTENT_KEY,
                content=arguments.CREATE_CONTENT_CONTENT_CONTENT,
                created_by=created_by,
            )

    @tag("controllers.content.create_content_bad_content")
    def test_create_content_bad_content(self) -> None:
        """Fail Case: Create a `Content` record with non JSON-compliant
        content."""

        with pytest.raises(ContentError):
            created_by = AuthModels.User.objects.get(
                username=arguments.CREATE_CONTENT_CONTENT_CREATED_BY
            )
            _ = controllers.Content.create_content(
                key=arguments.CREATE_CONTENT_CONTENT_KEY,
                content=arguments.CREATE_CONTENT_CONTENT_CONTENT_BAD_CONTENT,
                created_by=created_by,
            )
