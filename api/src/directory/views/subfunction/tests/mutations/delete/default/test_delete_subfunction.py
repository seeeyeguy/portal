"""
Collection of pytests for SubFunction's delete view endpoint.
"""

from typing import List

from django.contrib.auth.models import User
from django.test import tag
from django.urls import reverse
from rest_framework import status

from directory.controllers.SubFunction.tests.mutations.delete.default import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "directory",
    "subfunction",
    "views",
    "directory.subfunction.delete",
    "subfunction.delete.default",
    "views.TestDeleteSubFunction",
)
class TestDeleteSubFunction(MultiDBTestCase):
    """
    Tests for DELETE /v1/directory/subfunctions endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = User.objects.get(email__iexact=arguments.DELETE_SUBFUNCTION_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
        "portal/models/fixtures/users/users.json",
    ]

    url: str = reverse("directory.subfunction")

    @tag("views.subfunction.delete_subfunction")
    def test_delete_subfunction(self) -> None:
        """Success Case: Delete a `SubFunction` record."""

        request_url: str = (
            f"{self.url}?id={arguments.DELETE_SUBFUNCTION_SUBFUNCTION_ID}"
        )

        response = self.client.delete(
            request_url, headers={"content-type": "application/json"}
        )
        rows_affected = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rows_affected, arguments.DELETE_SUBFUNCTION_ROWS_AFFECTED)
