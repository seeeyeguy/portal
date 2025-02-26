"""
Collection of pytests for Tag's delete view endpoint.
"""

from typing import List

from django.contrib.auth.models import User
from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from directory.controllers.Tag.tests.mutations.delete.default import arguments


@tag(
    "directory",
    "tag",
    "views",
    "directory.tag.delete",
    "tag.delete.default",
    "views.TestDeleteTag",
)
class TestDeleteTag(TestCase):
    """
    Tests for DELETE /v1/directory/tags endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = User.objects.get(email__iexact=arguments.DELETE_TAG_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
        "portal/models/fixtures/users/users.json",
    ]

    url: str = reverse("directory.tag")

    @tag("views.tag.delete_tag")
    def test_delete_tag(self) -> None:
        """Success Case: Delete a `Tag` record."""

        request_url: str = f"{self.url}?id={arguments.DELETE_TAG_BY_ID}"
        response = self.client.delete(
            request_url, headers={"content-type": "application/json"}
        )

        rows_affected = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rows_affected, 1)
