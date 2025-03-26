"""
Collection of pytests for Function's delete view endpoint.
"""

from typing import List

from django.contrib.auth.models import User
from django.test import tag
from django.urls import reverse
from rest_framework import status

from directory.controllers.Function.tests.mutations.delete.default import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "directory",
    "function",
    "views",
    "directory.function.delete",
    "function.delete.default",
    "views.TestDeleteFunction",
)
class TestDeleteFunction(MultiDBTestCase):
    """
    Tests for DELETE /v1/directory/functions endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = User.objects.get(email__iexact=arguments.DELETE_FUNCTION_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/users/users.json",
    ]

    url: str = reverse("directory.function")

    @tag("views.function.delete_function")
    def test_delete_function(self) -> None:
        """Success Case: Delete a `Function` record."""

        request_url: str = f"{self.url}?id={arguments.DELETE_FUNCTION_BY_ID}"
        response = self.client.delete(
            request_url, headers={"content-type": "application/json"}
        )

        rows_affected = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rows_affected, 1)
