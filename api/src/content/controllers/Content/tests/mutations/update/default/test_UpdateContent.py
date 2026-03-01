"""
Collection of pytests for Content's update controller.
"""

from typing import List

import pytest

from django.contrib.auth import models as AuthModels
from django.test import tag

from content import controllers, models
from content.controllers.Content.tests.mutations.update.default import arguments
from content.exceptions import ContentError

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "content",
    "controllers.TestUpdateContent",
    "content.content.update",
    "content.update.default",
)
class TestUpdateContent(MultiDBTestCase):
    """Test suite for Content's update controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "content/controllers/Content/tests/mutations/update/default/fixtures/content.json",
        "content/controllers/Content/tests/mutations/update/default/fixtures/users.json",
    ]

    @tag("controllers.content.update_content")
    def test_update_content(self) -> None:
        """Success Case: Update a `Content` record."""

        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_CONTENT_UPDATED_BY_USER
        )
        content = controllers.Content.update_content(
            key=arguments.UPDATE_CONTENT_CONTENT_KEY,
            content=arguments.UPDATE_CONTENT_CONTENT_CONTENT,
            modified_by=user,
        )

        self.assertIsInstance(content, models.Content)
        self.assertEqual(content.key, arguments.UPDATE_CONTENT_CONTENT_KEY)
        self.assertEqual(content.content, arguments.UPDATE_CONTENT_CONTENT_CONTENT)
        self.assertEqual(content.modified_by, user)

    @tag("controllers.content.update_content_content_key_dne")
    def test_update_content_content_key_dne(self) -> None:
        """Fail Case: Update a `Content` record with a `key` that does not exist."""

        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_CONTENT_UPDATED_BY_USER
        )

        with pytest.raises(ContentError):
            controllers.Content.update_content(
                key=arguments.UPDATE_CONTENT_CONTENT_KEY_DNE,
                content=arguments.UPDATE_CONTENT_CONTENT_CONTENT,
                modified_by=user,
            )

    @tag("controllers.content.update_content_not_authorized")
    def test_update_content_not_authorized(self) -> None:
        """Fail Case: Update a `Content` record without proper permissions."""

        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_CONTENT_CONTENT_USER_NOT_AUTHORIZED
        )

        with pytest.raises(ContentError):
            controllers.Content.update_content(
                key=arguments.UPDATE_CONTENT_CONTENT_KEY,
                content=arguments.UPDATE_CONTENT_CONTENT_CONTENT,
                modified_by=user,
            )

    @tag("controllers.content.update_content_bad_content")
    def test_update_content_bad_content(self) -> None:
        """Fail Case: Update a `Content` record with bad content."""

        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_CONTENT_UPDATED_BY_USER
        )

        with pytest.raises(ContentError):
            controllers.Content.update_content(
                key=arguments.UPDATE_CONTENT_CONTENT_KEY,
                content=arguments.UPDATE_CONTENT_CONTENT_BAD_CONTENT,
                modified_by=user,
            )
