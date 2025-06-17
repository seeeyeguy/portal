"""
Collection of pytests for Request's delete view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from request.controllers.Request.tests.mutations.delete.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "request_app",
    "request",
    "views",
    "request_app.request.delete",
    "request.delete.default",
    "views.TestDeleteRequest",
)
class TestDeleteRequest(MultiDBTestCase):
    """
    Tests for DELETE /v1/request/request endpoint.
    """

    def setUp(self) -> None:

        super().setUp()

        self.client = APIClient()

        user = AuthModels.User.objects.get(
            email__iexact=arguments.DELETE_REQUEST_USER_EMAIL
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "request/controllers/Request/tests/mutations/delete/default/fixtures/users.json",
        "request/controllers/Request/tests/mutations/delete/default/fixtures/resources.json",
        "request/controllers/Request/tests/mutations/delete/default/fixtures/pointofcontacts.json",
        "request/controllers/Request/tests/mutations/delete/default/fixtures/requests.json",
        "request/controllers/Request/tests/mutations/delete/default/fixtures/transitions.json",
        "request/controllers/Request/tests/mutations/delete/default/fixtures/dispositions.json",
    ]

    url: str = reverse("request.request")

    @tag("views.request.delete_request")
    def test_delete_request(self) -> None:
        """Success Case: Create a delete `Request` record."""

        response = self.client.delete(
            f"{self.url}?id={arguments.DELETE_REQUEST_RESOURCE_ID}",
            data={},
            format="json",
        )

        rows_affected = response.json()

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(rows_affected, 1)

    @tag("controllers.request.delete_request_user_permissions_denied")
    def test_delete_request_user_permissions_denied(self) -> None:
        """Fail Case: Create a delete `Request` record with a `User` that
        does not have the appropriate permissions."""

        user = AuthModels.User.objects.get(
            email__iexact=arguments.DELETE_REQUEST_USER_EMAIL_INVALID_ROLE
        )
        self.client.force_login(user=user)

        response = self.client.delete(
            f"{self.url}?id={arguments.DELETE_REQUEST_RESOURCE_ID}",
            data={},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("controllers.request.delete_request_already_exists")
    def test_delete_request_request_already_exists(self) -> None:
        """Fail Case: Create a delete `Request` record for a `Resource` that
        already has an open request."""

        response = self.client.delete(
            f"{self.url}?id={arguments.DELETE_REQUEST_RESOURCE_ID_HAS_REQUEST_OPEN}",
            data={},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.request.delete_request_resource_dne")
    def test_delete_request_resource_dne(self) -> None:
        """Fail Case: Create a delete `Request` where
        the `Resource` does not exist for the given id."""

        response = self.client.delete(
            f"{self.url}?id={arguments.DELETE_REQUEST_RESOURCE_ID_DNE}",
            data={},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
