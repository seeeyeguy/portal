"""
Collection of pytests for Tag's update view endpoint.
"""

from typing import List

from django.contrib.auth.models import User
from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from directory.controllers.Tag.tests.mutations.update.default import arguments

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "directory",
    "tag",
    "views",
    "directory.tag.update",
    "tag.update.default",
    "views.TestUpdateTag",
)
class TestUpdateTag(TestCase):
    """
    Tests for PUT /v1/directory/tags endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = User.objects.get(email__iexact=arguments.UPDATE_TAG_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("directory.tag")

    @tag("views.tag.update_tag")
    def test_update_tag(self) -> None:
        """Success Case: Update a `Tag` record."""

        body: dict = {"label": arguments.UPDATE_TAG_LABEL}

        request_url: str = f"{self.url}?id={arguments.UPDATE_TAG_ID}"

        # Make request to update `Tag`.
        response = self.client.put(request_url, body, content_type="application/json")

        tag = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(tag, dict)

        # Remove dynamic datetime fields before comparison.
        del tag["created"]
        del tag["modified"]

        self.assertEqual(tag, arguments.UPDATE_TAG_EXPECTED_VALUES)

    @tag("views.tag.update_tag_record_dne")
    def test_update_tag_record_dne(self) -> None:
        """Fail Case: Update a `Tag` that does not exist."""

        body: dict = {"label": arguments.UPDATE_TAG_LABEL}

        request_url: str = f"{self.url}?id={arguments.UPDATE_TAG_ID_DNE}"

        # Make request to update `Tag`.
        response = self.client.put(request_url, body, content_type="application/json")
        # Ensure the response status code is 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.tag.update_tag_duplicate_label")
    def test_update_tag_duplicate_label(self) -> None:
        """Fail Case: Update a `Tag` record with a duplicate label."""

        body: dict = {"label": arguments.UPDATE_TAG_LABEL_DUPLICATE}

        request_url: str = f"{self.url}?id={arguments.UPDATE_TAG_ID}"

        # Make request to update `Tag`.
        response = self.client.put(request_url, body, content_type="application/json")
        # Ensure the response status code is 400.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.tag.update_tag_empty_label")
    def test_update_tag_empty_label(self) -> None:
        """Fail Case: Update a `Tag` record with an empty label."""

        body: dict = {"label": ""}

        request_url: str = f"{self.url}?id={arguments.UPDATE_TAG_ID}"

        # Make request to update `Tag`.
        response = self.client.put(request_url, body, content_type="application/json")
        # Ensure the response status code is 400.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
