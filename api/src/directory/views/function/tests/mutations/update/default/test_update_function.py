"""
Collection of pytests for Function's update view endpoint.
"""

import pytest
from typing import List

from django.contrib.auth.models import User
from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from directory.controllers import Function
from directory.controllers.Function.tests.mutations.update.default import arguments
from directory.exceptions import DirectoryError
from directory.models.Function import Function as FunctionModel
from directory.models.Function.serializers import FunctionSerializer


@tag(
    "directory",
    "function",
    "views",
    "directory.function.update",
    "function.update.default",
    "views.TestUpdateFunction",
)
class TestUpdateFunction(TestCase):
    """
    Tests for PUT /v1/directory/functions endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = User.objects.get(email=arguments.UPDATE_FUNCTION_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/users/users.json",
    ]

    url: str = reverse("directory.function")

    @tag("views.function.update_function")
    def test_update_function(self) -> None:
        """Success Case: Update a `Function` record."""

        body: dict = {
            "name": arguments.UPDATE_FUNCTION_NAME,
            "description": arguments.UPDATE_FUNCTION_DESCRIPTION,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_FUNCTION_ID}"
        response = self.client.put(
            request_url, data=body, content_type="application/json"
        )

        data = response.json()

        # Remove dynamic datetime field before comparison.
        del data["modified"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, arguments.UPDATE_FUNCTION_EXPECTED_VALUES)

    @tag("views.function.update_function_record_dne")
    def test_update_function_record_dne(self) -> None:
        """Fail Case: Update a `Function` that does not exist."""

        body = {
            "name": arguments.UPDATE_FUNCTION_NAME,
            "description": arguments.UPDATE_FUNCTION_DESCRIPTION,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_FUNCTION_ID_DNE}"
        response = self.client.put(
            request_url, data=body, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.function.update_function_duplicate_name")
    def test_update_function_duplicate_name(self) -> None:
        """Fail Case: Update a `Function` record with a duplicate name."""

        body = {
            "name": arguments.UPDATE_FUNCTION_DUPLICATE_NAME,
            "description": arguments.UPDATE_FUNCTION_DESCRIPTION,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_FUNCTION_ID_DUPLICATE}"
        response = self.client.put(
            request_url, data=body, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
