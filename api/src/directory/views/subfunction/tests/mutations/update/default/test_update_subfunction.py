"""
Collection of pytests for SubFunction's update view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from directory.controllers.SubFunction.tests.mutations.update.default import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "directory",
    "subfunction",
    "views",
    "directory.subfunction.update",
    "subfunction.update.default",
    "views.TestUpdateSubFunction",
)
class TestUpdateSubFunction(MultiDBTestCase):
    """
    Tests for PUT /v1/directory/subfunctions endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            email=arguments.UPDATE_SUBFUNCTION_USER_EMAIL
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
        "portal/models/fixtures/users/users.json",
    ]

    url: str = reverse("directory.subfunction")

    @tag("views.subfunction.update_subfunction")
    def test_update_subfunction(self) -> None:
        """Success Case: Update a `SubFunction` record."""

        request_url: str = f"{self.url}?id={arguments.UPDATE_SUBFUNCTION_ID}"
        response = self.client.put(
            request_url,
            {
                "name": arguments.UPDATE_SUBFUNCTION_NAME,
                "description": arguments.UPDATE_SUBFUNCTION_DESCRIPTION,
                "function": arguments.UPDATE_SUBFUNCTION_FUNCTION_ID,
            },
            content_type="application/json",
        )
        subfunction = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Remove dynamic datetime field before comparison.
        del subfunction["modified"]

        self.assertDictEqual(subfunction, arguments.VALID_SUBFUNCTION)

    @tag("views.subfunction.update_subfunction_record_dne")
    def test_update_subfunction_record_dne(self) -> None:
        """Fail Case: Update a `SubFunction` that does not exist."""

        request_url: str = f"{self.url}?id={arguments.UPDATE_SUBFUNCTION_ID_DNE}"
        response = self.client.put(
            request_url,
            {
                "name": arguments.UPDATE_SUBFUNCTION_NAME,
                "description": arguments.UPDATE_SUBFUNCTION_DESCRIPTION,
                "function": arguments.UPDATE_SUBFUNCTION_FUNCTION_ID,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.subfunction.update_subfunction_duplicate_name")
    def test_update_subfunction_duplicate_name(self) -> None:
        """Fail Case: Update a `SubFunction` record with a duplicate name."""

        request_url: str = f"{self.url}?id={arguments.UPDATE_SUBFUNCTION_ID}"
        response = self.client.put(
            request_url,
            {
                "name": arguments.UPDATE_SUBFUNCTION_DUPLICATE_NAME,
                "description": arguments.UPDATE_SUBFUNCTION_DESCRIPTION,
                "function": arguments.UPDATE_SUBFUNCTION_FUNCTION_ID,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.subfunction.update_subfunction_function_dne")
    def test_update_subfunction_function_dne(self) -> None:
        """Fail Case: Update a `SubFunction` record with a given
        function id where that `Function` does not exist."""

        request_url: str = f"{self.url}?id={arguments.UPDATE_SUBFUNCTION_ID}"
        response = self.client.put(
            request_url,
            {
                "name": arguments.UPDATE_SUBFUNCTION_NAME,
                "description": arguments.UPDATE_SUBFUNCTION_DESCRIPTION,
                "function": arguments.UPDATE_SUBFUNCTION_FUNCTION_ID_DNE,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
