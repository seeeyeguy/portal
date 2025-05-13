"""
Collection of pytests for Access's update controller.
"""

from typing import List

from django.test import tag

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "users",
    "access",
    "controllers.TestRevokeAccess",
    "users.access.update",
    "access.update.default",
)
class TestRevokeAccess(MultiDBTestCase):
    """Test suite for `Access`'s update controller."""

    fixtures: List[str] = []

    @tag("controllers.access.revoke_access")
    def test_revoke_access(self) -> None:
        """Success Case: Revoke an `Access` record, given its id."""

    @tag("controllers.access.revoke_access_access_dne")
    def test_revoke_access_access_dne(self) -> None:
        """Fail Case: Revoke an `Access` record, given its id where
        that `Access` does not exist."""

    @tag("controllers.access.revoke_access_not_authenticated")
    def test_revoke_access_not_authenticated(self) -> None:
        """Fail Case: Revoke an `Access` record where the given
        admin is not authenticated."""

    @tag("controllers.access.revoke_access_permissions_denied")
    def test_revoke_access_permissions_denied(self) -> None:
        """Fail Case: Revoke an `Access` record, given its id where
        the given admin does not have the appropriate permissions."""
