"""
Collection of pytests for Content's delete view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from content.controllers.Content.tests.mutations.delete.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "content",
    "views",
    "content.content.delete",
    "content.delete.default",
    "views.TestDeleteContent",
)
class TestDeleteContent(MultiDBTestCase):
    """
    Tests for DELETE /v1/content/content endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            email=arguments.DELETE_CONTENT_DELETED_BY_USER
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "content/controllers/Content/tests/mutations/delete/default/fixtures/content.json",
        "content/controllers/Content/tests/mutations/delete/default/fixtures/users.json",
    ]

    url: str = reverse("content.content")

    @tag("views.content.delete_content")
    def test_delete_content(self) -> None:
        """Success Case: DELETE /v1/content/content."""

        response = self.client.delete(
            f"{self.url}?key={arguments.DELETE_CONTENT_CONTENT_KEY}",
            headers={"content-type": "application/json"},
        )

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, 1)
