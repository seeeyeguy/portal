"""
Collection of pytests for Content's update view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from content.controllers.Content.tests.mutations.update.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "content",
    "views",
    "content.content.update",
    "content.update.default",
    "views.TestUpdateContent",
)
class TestUpdateContent(MultiDBTestCase):
    """
    Tests for PUT /v1/content/content endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_CONTENT_UPDATED_BY_USER
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "content/controllers/Content/tests/mutations/update/default/fixtures/content.json",
        "content/controllers/Content/tests/mutations/update/default/fixtures/users.json",
    ]

    url: str = reverse("content.content")

    @tag("views.content.update_content")
    def test_update_content(self) -> None:
        """Success Case: Update a `Content` record."""

        url = f"{self.url}?key={arguments.UPDATE_CONTENT_CONTENT_KEY}"
        body = {
            "content": arguments.UPDATE_CONTENT_CONTENT_CONTENT,
        }

        response = self.client.put(url, data=body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        self.assertEqual(data["key"], arguments.UPDATE_CONTENT_CONTENT_KEY)
        self.assertEqual(data["content"], arguments.UPDATE_CONTENT_CONTENT_CONTENT)

    @tag("views.content.update_content_content_key_dne")
    def test_update_content_content_key_dne(self) -> None:
        """Fail Case: Update a `Content` record with a `key` that does not exist."""

        url = f"{self.url}?key={arguments.UPDATE_CONTENT_CONTENT_KEY_DNE}"
        body = {
            "content": arguments.UPDATE_CONTENT_CONTENT_CONTENT,
        }

        response = self.client.put(url, data=body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.content.update_content_not_authorized")
    def test_update_content_not_authorized(self) -> None:
        """Fail Case: Update a `Content` record without proper permissions."""

        self.client.force_login(
            user=AuthModels.User.objects.get(
                username=arguments.UPDATE_CONTENT_CONTENT_USER_NOT_AUTHORIZED
            )
        )

        url = f"{self.url}?key={arguments.UPDATE_CONTENT_CONTENT_KEY}"
        body = {
            "content": arguments.UPDATE_CONTENT_CONTENT_CONTENT,
        }

        response = self.client.put(url, data=body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("views.content.update_content_bad_content")
    def test_update_content_bad_content(self) -> None:
        """Fail Case: Update a `Content` record with bad content."""

        url = f"{self.url}?key={arguments.UPDATE_CONTENT_CONTENT_KEY}"
        body = {
            "content": arguments.UPDATE_CONTENT_CONTENT_BAD_CONTENT,
        }

        response = self.client.put(url, data=body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
