"""
Collection of pytests for Tag's create view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from directory.controllers.Tag.tests.mutations.create.default import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "directory",
    "tag",
    "views",
    "directory.tag.create",
    "tag.create.default",
    "views.TestCreateTag",
)
class TestCreateTag(MultiDBTestCase):
    """
    Tests for POST /v1/directory/tags endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(username=arguments.CREATE_TAG_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        "portal/models/fixtures/tags/tags.json",
        "portal/models/fixtures/users/users.json",
    ]

    url: str = reverse("directory.tag")

    @tag("views.tag.create_tag")
    def test_create_tag(self) -> None:
        """Success Case: Create a `Tag` record."""

        body: dict = {"label": arguments.CREATE_TAG_LABEL}

        response = self.client.post(self.url, body, content_type="application/json")

        tag_record = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(tag_record, dict)

        del tag_record["id"]
        del tag_record["created"]
        del tag_record["modified"]

        self.assertEqual(tag_record, arguments.CREATE_TAG_EXPECTED_VALUE)

    @tag("views.tag.create_tag_duplicate_label")
    def test_create_tag_duplicate_label(self) -> None:
        """Fail Case: Create a `Tag` record with a duplicate label."""

        body: dict = {"label": arguments.CREATE_DUPLICATE_TAG}

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.tag.create_tag_empty_label")
    def test_create_tag_empty_label(self) -> None:
        """Fail Case: Create a `Tag` record with an empty label."""

        request_url: str = f"{self.url}"
        response = self.client.post(
            request_url,
            {"label": ""},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
