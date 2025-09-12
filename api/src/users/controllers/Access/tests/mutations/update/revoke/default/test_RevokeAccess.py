"""
Collection of pytests for Access's revoke update controller.
"""

import pytest
from typing import cast, List

from django.contrib.auth import models as AuthModels
from django.db.models import QuerySet
from django.test import tag

from users import controllers, exceptions, models
from users.controllers.Access.tests.mutations.update.revoke.default import arguments
from users.models.Access.serializers import AccessSerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "users",
    "access",
    "controllers.TestRevokeAccess",
    "users.access.revoke.update",
    "users.access.update",
    "access.update.default",
)
class TestRevokeAccess(MultiDBTestCase):
    """Test suite for `Access`'s revoke update controller."""

    fixtures: List[str] = [*COMMON_FIXTURES]

    @tag("controllers.access.revoke_access")
    def test_revoke_access(self) -> None:
        """Success Case: Revoke an `Access` record, given its id."""

        admin = AuthModels.User.objects.get(
            email=arguments.REVOKE_ACCESS_ADMIN_USER_EMAIL
        )

        access_records, rows_affected = controllers.Access.revoke_accesses(
            accesses=[arguments.REVOKE_ACCESS_ACCESS_ID],
            admin=admin,
        )

        self.assertIsInstance(access_records, QuerySet[models.Access])
        self.assertIsNotNone(
            cast(models.Access, access_records.first()).access_revoked_date
        )
        self.assertEqual(rows_affected, arguments.REVOKE_ACCESS_EXPECTED_ROWS_AFFECTED)

        data = AccessSerializer(access_records, many=True).data
        del data[0]["access_revoked_date"]

        self.assertDictEqual(data[0], arguments.REVOKED_ACCESS_EXPECTED_ACCESS)

    @tag("controllers.access.revoke_access_access_dne")
    def test_revoke_access_access_dne(self) -> None:
        """Fail Case: Revoke an `Access` record, given its id where
        that `Access` does not exist."""

        admin = AuthModels.User.objects.get(
            email=arguments.REVOKE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.revoke_accesses(
                accesses=[arguments.REVOKE_ACCESS_ACCESS_ID_DNE], admin=admin
            )

    @tag("controllers.access.revoke_access_not_authenticated")
    def test_revoke_access_not_authenticated(self) -> None:
        """Fail Case: Revoke an `Access` record where the given
        admin is not authenticated."""

        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.revoke_accesses(
                accesses=[arguments.REVOKE_ACCESS_ACCESS_ID],
                admin=cast(AuthModels.User, AuthModels.AnonymousUser()),
            )

    @tag("controllers.access.revoke_access_permissions_denied")
    def test_revoke_access_permissions_denied(self) -> None:
        """Fail Case: Revoke an `Access` record, given its id where
        the given admin does not have the appropriate permissions."""

        admin = AuthModels.User.objects.get(
            email=arguments.REVOKE_ACCESS_NON_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.revoke_accesses(
                accesses=[arguments.REVOKE_ACCESS_ACCESS_ID], admin=admin
            )

    @tag("controllers.access.revoke_access_access_belongs_to_admin")
    def test_revoke_access_access_belongs_to_admin(self) -> None:
        """Fail Case: Revoke an `Access` record, given its id where
        the given access id belongs to the given admin."""

        admin = AuthModels.User.objects.get(
            email=arguments.REVOKE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.revoke_accesses(
                accesses=[arguments.REVOKE_ACCESS_ADMIN_ACCESS_ID], admin=admin
            )
