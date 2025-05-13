"""
Collection of pytests for Access's update view endpoint.
"""

from typing import List

# NEED TO REMOVE pylint-disable AFTER IMPLEMENTATION.
# pylint: disable=useless-parent-delegation
from django.test import tag
from django.urls import reverse

from manager.utils.tests import MultiDBTestCase


@tag(
    "user",
    "access",
    "views",
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

    fixtures: List[str] = []

    url: str = reverse("users.access")

    @tag("views.access.revoke_access")
    def test_revoke_access(self) -> None:
        """Success Case: Revoke an `Access` record, given its id."""

    @tag("views.access.revoke_access_access_dne")
    def test_revoke_access_access_dne(self) -> None:
        """Fail Case: Revoke an `Access` record, given its id where
        that `Access` does not exist."""

    @tag("views.access.revoke_access_permissions_denied")
    def test_revoke_access_permissions_denied(self) -> None:
        """Fail Case: Revoke an `Access` record, given its id where
        request.`User` does not have the appropriate permissions."""
