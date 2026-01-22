"""
Collection of pytests for Content's create view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from content.controllers.Content.tests.mutations.create.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "content",
    "views",
    "content.content.create",
    "content.create.default",
    "views.TestCreateContent",
)
class TestCreateContent(MultiDBTestCase):
    """
    Tests for POST /v1/content/content endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            email=arguments.CREATE_CONTENT_CONTENT_CREATED_BY
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "content/controllers/Content/tests/mutations/create/default/fixtures/users.json",
    ]

    url: str = reverse("content.content")

    body: dict = {
        "key": arguments.CREATE_CONTENT_CONTENT_KEY,
        "content": arguments.CREATE_CONTENT_CONTENT_CONTENT,
    }

    @tag("controllers.content.create_content")
    def test_create_content(self) -> None:
        """Success Case: Create a `Content` record."""

        response = self.client.post(
            self.url,
            data=self.body,
            content_type="application/json",
        )

        content = response.json()

        self.assertEqual(content["key"], self.body["key"])
        self.assertEqual(content["content"], self.body["content"])

    @tag("controllers.content.create_content_bad_content")
    def test_create_content_bad_content(self) -> None:
        """Fail Case: Create a `Content` record with non JSON-compliant
        content."""

        response = self.client.post(
            self.url,
            data={
                **self.body,
                "content": arguments.CREATE_CONTENT_CONTENT_CONTENT_BAD_CONTENT,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
