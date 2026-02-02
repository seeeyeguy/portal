"""
Collection of pytests for Content's delete controller.
"""

from typing import List

import pytest

from django.contrib.auth import models as AuthModels
from django.test import tag

from content import controllers
from content.controllers.Content.tests.mutations.delete.default import arguments
from content.exceptions import ContentError

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "content",
    "controllers.TestDeleteContent",
    "content.content.delete",
    "content.delete.default",
)
class TestDeleteContent(MultiDBTestCase):
    """Test suite for Content's delete controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "content/controllers/Content/tests/mutations/delete/default/fixtures/content.json",
        "content/controllers/Content/tests/mutations/delete/default/fixtures/users.json",
    ]

    @tag("controllers.content.delete_content")
    def test_delete_content(self) -> None:
        """Success Case: Delete a `Content` record."""

        user = AuthModels.User.objects.get(
            email=arguments.DELETE_CONTENT_DELETED_BY_USER
        )
        rows_affected = controllers.Content.delete_content(
            key=arguments.DELETE_CONTENT_CONTENT_KEY,
            deleted_by=user,
        )

        self.assertEqual(rows_affected, 1)

    @tag("controllers.content.delete_content_not_authorized")
    def test_delete_content_not_authorized(self) -> None:
        """Fail Case: Attempt to delete a `Content` record without proper permissions."""

        with pytest.raises(ContentError):
            user = AuthModels.User.objects.get(
                email=arguments.DELETE_CONTENT_CONTENT_USER_NOT_AUTHORIZED
            )
            controllers.Content.delete_content(
                key=arguments.DELETE_CONTENT_CONTENT_KEY,
                deleted_by=user,
            )
