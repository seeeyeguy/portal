"""
Collection of pytests for Function's create view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from directory.controllers.Function.tests.mutations.create.default import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "directory",
    "function",
    "views",
    "directory.function.create",
    "function.create.default",
    "views.TestCreateFunction",
)
class TestCreateFunction(MultiDBTestCase):
    """
    Tests for POST /v1/directory/functions endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            username=arguments.CREATE_FUNCTION_USER_EMAIL
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
        "portal/models/fixtures/users/users.json",
        "portal/models/fixtures/roles/roles.json",
        "portal/models/fixtures/stages/stages.json",
        "portal/models/fixtures/accesses/accesses.json",
    ]

    url: str = reverse("directory.function")

    @tag("views.function.create_function")
    def test_create_function(self) -> None:
        """Success Case: Create a `Function` record."""

        body: dict = {
            "name": arguments.CREATE_FUNCTION_NAME,
            "description": arguments.CREATE_FUNCTION_DESCRIPTION,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        function = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(function, dict)

        # Remove dynamic primary key and
        # datetime fields before comparison.
        del function["created"]
        del function["id"]
        del function["modified"]

        self.assertEqual(function, arguments.CREATE_FUNCTION_EXPECTED_VALUES)

    @tag("views.function.create_function_duplicate_name")
    def test_create_function_duplicate_name(self) -> None:
        """Fail Case: Create a `Function` record with a duplicate name."""

        body: dict = {
            "name": arguments.CREATE_FUNCTION_DUPLICATE_NAME,
            "description": arguments.CREATE_FUNCTION_DESCRIPTION,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
