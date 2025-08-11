"""
Collection of pytests for Access's revoke update view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from users.controllers.Access.tests.mutations.update.revoke.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "users",
    "access",
    "views",
    "users.access.update.revoke",
    "users.access.update",
    "access.update.default",
    "views.TestRevokeAccess",
)
class TestRevokeAccess(MultiDBTestCase):
    """
    Tests for PUT /v1/users/access endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            email=arguments.REVOKE_ACCESS_ADMIN_USER_EMAIL
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("users.access")

    @tag("views.access.revoke_access")
    def test_revoke_access(self) -> None:
        """Success Case: Revoke an `Access` record, given its id."""

        request_url = f"{self.url}?id={arguments.REVOKE_ACCESS_ACCESS_ID}"

        response = self.client.put(request_url, content_type="application/json")

        access = response.json()
        access_revoked_date = access.pop("access_revoked_date")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertDictEqual(access, arguments.REVOKED_ACCESS_EXPECTED_ACCESS)

        self.assertIsNotNone(access_revoked_date)

    @tag("views.access.revoke_access_access_dne")
    def test_revoke_access_access_dne(self) -> None:
        """Fail Case: Revoke an `Access` record, given its id where
        that `Access` does not exist."""

        request_url = f"{self.url}?id={arguments.REVOKE_ACCESS_ACCESS_ID_DNE}"

        response = self.client.put(request_url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.access.revoke_access_access_belongs_to_admin")
    def test_revoke_access_access_belongs_to_admin(self) -> None:
        """Fail Case: Revoke an `Access` record, given its id where
        the given access id belongs to the given admin."""

        request_url = f"{self.url}?id={arguments.REVOKE_ACCESS_ADMIN_ACCESS_ID}"

        response = self.client.put(request_url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.access.revoke_access_permissions_denied")
    def test_revoke_access_permissions_denied(self) -> None:
        """Fail Case: Revoke an `Access` record, given its id where
        request.`User` does not have the appropriate permissions."""

        user = AuthModels.User.objects.get(
            email=arguments.REVOKE_ACCESS_NON_ADMIN_USER_EMAIL
        )

        self.client.force_login(user=user)

        request_url = f"{self.url}?id={arguments.REVOKE_ACCESS_ACCESS_ID}"

        response = self.client.put(request_url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("views.access.revoke_access_not_authenticated")
    def test_revoke_access_not_authenticated(self) -> None:
        """Fail Case: Revoke an `Access` record where the given
        admin is not authenticated."""

        self.client.logout()

        request_url = f"{self.url}?id={arguments.REVOKE_ACCESS_ACCESS_ID}"

        response = self.client.put(request_url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
