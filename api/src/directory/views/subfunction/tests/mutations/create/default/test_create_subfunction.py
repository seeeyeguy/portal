"""
Collection of pytests for SubFunction's create view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from directory.controllers.SubFunction.tests.mutations.create.default import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "directory",
    "subfunction",
    "views",
    "directory.subfunction.create",
    "subfunction.create.default",
    "views.TestCreateSubFunction",
)
class TestCreateSubFunction(MultiDBTestCase):
    """
    Tests for POST /v1/directory/subfunctions endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            email=arguments.CREATE_SUBFUNCTION_USER_EMAIL
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
        "portal/models/fixtures/users/users.json",
    ]

    url: str = reverse("directory.subfunction")

    @tag("views.subfunction.create_subfunction")
    def test_create_subfunction(self) -> None:
        """Success Case: Create a `SubFunction` record."""

        body: dict = {
            "name": arguments.CREATE_SUBFUNCTION_NAME,
            "description": arguments.CREATE_SUBFUNCTION_DESCRIPTION,
            "function": arguments.CREATE_SUBFUNCTION_FUNCTION_ID,
        }

        # Make request to create `SubFunction`.
        response = self.client.post(self.url, body, content_type="application/json")

        subfunction = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(subfunction, dict)

        # Remove dynamic subfunction's primary key, datetime fields, function name,
        # function datetime fields before comparison.
        del subfunction["id"]
        del subfunction["created"]
        del subfunction["modified"]
        del subfunction["function"]["created"]
        del subfunction["function"]["modified"]

        self.assertEqual(subfunction, arguments.CREATE_SUBFUNCTION_EXPECTED_VALUES)

    @tag("views.subfunction.create_subfunction_duplicate_name")
    def test_create_subfunction_duplicate_name(self) -> None:
        """Fail Case: Create a `SubFunction` record with a duplicate name."""

        body: dict = {
            "name": arguments.CREATE_SUBFUNCTION_DUPLICATE_NAME,
            "description": arguments.CREATE_SUBFUNCTION_DESCRIPTION,
            "function": arguments.CREATE_SUBFUNCTION_FUNCTION_ID,
        }

        # Make request to create `SubFunction`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 400.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.subfunction.create_subfunction_function_dne")
    def test_create_subfunction_function_dne(self) -> None:
        """Fail Case: Create a `SubFunction` record with a given
        function id where that `Function` does not exist."""

        body: dict = {
            "name": arguments.CREATE_SUBFUNCTION_NAME,
            "description": arguments.CREATE_SUBFUNCTION_DESCRIPTION,
            "function": arguments.CREATE_SUBFUNCTION_FUNCTION_DNE,
        }

        # Make request to create `SubFunction`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
