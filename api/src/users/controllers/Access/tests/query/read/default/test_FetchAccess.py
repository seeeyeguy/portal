"""
Collection of pytests for Access's fetch controller.
"""

import pytest
from typing import cast, List

from django.contrib.auth import models as AuthModels
from django.db.models import QuerySet
from django.test import tag

from users import controllers, exceptions, models
from users.controllers.Access.tests.query.read.default import arguments
from users.models.Access.serializers import AccessSerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "users",
    "access",
    "controllers.TestFetchAccess",
    "users.access.fetch",
    "access.fetch.default",
)
class TestFetchAccess(MultiDBTestCase):
    """Test suite for `Access`'s fetch controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "users/controllers/Access/tests/query/read/default/fixtures/users.json",
        "users/controllers/Access/tests/query/read/default/fixtures/accesses.json",
    ]

    def setUp(self) -> None:
        super().setUp()

        self.access_records = {}
        for access_id in arguments.FETCH_ACCESSES_ALL_ACCESS_ACCESS_IDS:
            serialized_access = AccessSerializer(
                models.Access.objects.get(id=access_id)
            ).data
            self.access_records[access_id] = serialized_access

    @tag("controllers.access.fetch_access")
    def test_fetch_access(self) -> None:
        """Success Case: Fetch an `Access` record, given its id."""

        admin = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_ADMIN_USER_EMAIL
        )

        access_record = controllers.Access.fetch_accesses(
            access=arguments.FETCH_ACCESS_BY_ID_ACCESS_ID,
            user=None,
            role_levels=None,
            subfunctions=None,
            include_revoked=None,
            admin=admin,
        )

        data = AccessSerializer(access_record).data

        self.assertIsInstance(access_record, models.Access)

        self.assertDictEqual(
            data, self.access_records[arguments.FETCH_ACCESS_BY_ID_ACCESS_ID]
        )

    @tag("controllers.access.fetch_accesses")
    def test_fetch_accesses(self) -> None:
        """Success Case: Fetch all `Access` records."""

        admin = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_ADMIN_USER_EMAIL
        )

        access_records = controllers.Access.fetch_accesses(
            access=None,
            user=None,
            role_levels=None,
            subfunctions=None,
            include_revoked=None,
            admin=admin,
        )

        self.assertIsInstance(access_records, QuerySet[models.Access])

        self.assertEqual(
            access_records.count(),  # type: ignore[union-attr]
            len(arguments.FETCH_ACCESSES_VALID_ACCESS_RECORD_IDS),
        )

        for access in access_records:  # type: ignore[union-attr]
            self.assertIsInstance(access, models.Access)

            access_id: int = access.id

            self.assertIn(access_id, arguments.FETCH_ACCESSES_VALID_ACCESS_RECORD_IDS)

            serialized_access = AccessSerializer(access).data
            expected_access = self.access_records[access_id]

            self.assertEqual(
                serialized_access,
                expected_access,
            )

    @tag("controllers.access.fetch_user_accesses")
    def test_fetch_user_accesses(self) -> None:
        """Success Case: Fetch all `Access` records for a `User`."""

        admin = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_ADMIN_USER_EMAIL
        )

        access_records = controllers.Access.fetch_accesses(
            access=None,
            user=arguments.FETCH_ACCESSES_BY_USER_USER_EMAIL,
            role_levels=None,
            subfunctions=None,
            include_revoked=None,
            admin=admin,
        )

        self.assertIsInstance(access_records, QuerySet[models.Access])

        self.assertEqual(
            access_records.count(),  # type: ignore[union-attr]
            len(arguments.FETCH_ACCESSES_FOR_USER_ACCESS_RECORD_IDS),
        )

        for access in access_records:  # type: ignore[union-attr]
            self.assertIsInstance(access, models.Access)

            access_id: int = access.id

            self.assertIn(
                access_id, arguments.FETCH_ACCESSES_FOR_USER_ACCESS_RECORD_IDS
            )

            serialized_access = AccessSerializer(access).data
            expected_access = self.access_records[access_id]

            self.assertEqual(serialized_access, expected_access)

    @tag("controllers.access.fetch_roles_accesses")
    def test_fetch_roles_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s."""

        admin = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_ADMIN_USER_EMAIL
        )

        access_records = controllers.Access.fetch_accesses(
            access=None,
            user=None,
            role_levels=arguments.FETCH_ACCESSES_WITH_ROLE_LEVELS_ROLE_LEVELS,
            subfunctions=None,
            include_revoked=None,
            admin=admin,
        )

        self.assertIsInstance(access_records, QuerySet[models.Access])

        self.assertEqual(
            access_records.count(),  # type: ignore[union-attr]
            len(arguments.FETCH_ACCESSES_FOR_ROLE_LEVELS_ACCESS_RECORD_IDS),
        )

        for access in access_records:  # type: ignore[union-attr]
            self.assertIsInstance(access, models.Access)

            access_id: int = access.id

            self.assertIn(
                access_id, arguments.FETCH_ACCESSES_FOR_ROLE_LEVELS_ACCESS_RECORD_IDS
            )

            serialized_access = AccessSerializer(access).data
            expected_access = self.access_records[access_id]

            self.assertEqual(serialized_access, expected_access)

    @tag("controllers.access.fetch_subfunctions_accesses")
    def test_fetch_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `SubFunction`s."""

        admin = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_ADMIN_USER_EMAIL
        )

        access_records = controllers.Access.fetch_accesses(
            access=None,
            user=None,
            role_levels=None,
            subfunctions=arguments.FETCH_ACCESSES_WITH_SUBFUNCTIONS_SUBFUNCTIONS,
            include_revoked=None,
            admin=admin,
        )

        self.assertIsInstance(access_records, QuerySet[models.Access])
        self.assertEqual(
            access_records.count(),  # type: ignore[union-attr]
            len(arguments.FETCH_ACCESSES_FOR_SUBFUNCTIONS_ACCESS_RECORD_IDS),
        )

        for access in access_records:  # type: ignore[union-attr]
            self.assertIsInstance(access, models.Access)

            access_id: int = access.id

            self.assertIn(
                access_id, arguments.FETCH_ACCESSES_FOR_SUBFUNCTIONS_ACCESS_RECORD_IDS
            )

            serialized_access = AccessSerializer(access).data
            expected_access = self.access_records[access_id]

            self.assertEqual(serialized_access, expected_access)

    @tag("controllers.access.fetch_user_roles_accesses")
    def test_fetch_user_roles_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s for a `User`."""

        admin = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_ADMIN_USER_EMAIL
        )

        access_records = controllers.Access.fetch_accesses(
            access=None,
            user=arguments.FETCH_ACCESSES_WITH_USER_AND_ROLES_USER_EMAIL,
            role_levels=arguments.FETCH_ACCESSES_WITH_USER_AND_ROLE_LEVELS_ROLE_LEVELS,
            subfunctions=None,
            include_revoked=None,
            admin=admin,
        )

        self.assertIsInstance(access_records, QuerySet[models.Access])

        self.assertEqual(
            access_records.count(),  # type: ignore[union-attr]
            len(arguments.FETCH_ACCESSES_WITH_USER_AND_ROLE_LEVELS_ACCESS_RECORD_IDS),
        )

        for access in access_records:  # type: ignore[union-attr]
            self.assertIsInstance(access, models.Access)

            access_id: int = access.id

            self.assertIn(
                access_id,
                arguments.FETCH_ACCESSES_WITH_USER_AND_ROLE_LEVELS_ACCESS_RECORD_IDS,
            )

            serialized_access = AccessSerializer(access).data
            expected_access = self.access_records[access_id]

            self.assertEqual(serialized_access, expected_access)

    @tag("controllers.access.fetch_user_subfunctions_accesses")
    def test_fetch_user_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `SubFunction`s for a `User`."""

        admin = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_ADMIN_USER_EMAIL
        )

        access_records = controllers.Access.fetch_accesses(
            access=None,
            user=arguments.FETCH_ACCESSES_WITH_USER_AND_SUBFUNCTIONS_USER_EMAIL,
            role_levels=None,
            subfunctions=arguments.FETCH_ACCESSES_WITH_USER_AND_SUBFUNCTIONS_SUBFUNCTIONS,
            include_revoked=None,
            admin=admin,
        )

        self.assertIsInstance(access_records, QuerySet[models.Access])

        self.assertEqual(
            access_records.count(),  # type: ignore[union-attr]
            len(arguments.FETCH_ACCESSES_WITH_USER_AND_SUBFUNCTIONS_ACCESS_RECORD_IDS),
        )

        for access in access_records:  # type: ignore[union-attr]
            self.assertIsInstance(access, models.Access)

            access_id: int = access.id

            self.assertIn(
                access_id,
                arguments.FETCH_ACCESSES_WITH_USER_AND_SUBFUNCTIONS_ACCESS_RECORD_IDS,
            )

            serialized_access = AccessSerializer(access).data
            expected_access = self.access_records[access_id]

            self.assertEqual(serialized_access, expected_access)

    @tag("controllers.access.fetch_user_roles_subfunctions_accesses")
    def test_fetch_user_roles_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s and `SubFunction`s for a `User`."""

        admin = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_ADMIN_USER_EMAIL
        )

        access_records = controllers.Access.fetch_accesses(
            access=None,
            user=arguments.FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_USER_EMAIL,
            role_levels=arguments.FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_ROLE_LEVELS,
            subfunctions=arguments.FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_SUBFUNCTIONS,
            include_revoked=None,
            admin=admin,
        )

        self.assertIsInstance(access_records, QuerySet[models.Access])

        self.assertEqual(
            access_records.count(),  # type: ignore[union-attr]
            len(
                arguments.FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_ACCESS_RECORD_IDS
            ),
        )

        for access in access_records:  # type: ignore[union-attr]
            self.assertIsInstance(access, models.Access)

            access_id: int = access.id

            self.assertIn(
                access_id,
                arguments.FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_ACCESS_RECORD_IDS,
            )

            serialized_access = AccessSerializer(access).data
            expected_access = self.access_records[access_id]

            self.assertEqual(serialized_access, expected_access)

    @tag("controllers.access.fetch_accesses_include_revoked")
    def test_fetch_accesses_include_revoked(self) -> None:
        """Success Case: Fetch all `Access` records, including
        revoked `Access` records."""

        admin = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_ADMIN_USER_EMAIL
        )

        access_records = controllers.Access.fetch_accesses(
            access=None,
            user=None,
            role_levels=None,
            subfunctions=None,
            include_revoked=True,
            admin=admin,
        )

        self.assertIsInstance(access_records, QuerySet[models.Access])

        self.assertEqual(
            access_records.count(),  # type: ignore[union-attr]
            len(arguments.FETCH_ACCESSES_ALL_ACCESS_ACCESS_IDS),
        )

        for access in access_records:  # type: ignore[union-attr]
            self.assertIsInstance(access, models.Access)

            access_id: int = access.id

            self.assertIn(access_id, arguments.FETCH_ACCESSES_ALL_ACCESS_ACCESS_IDS)

            serialized_access = AccessSerializer(access).data
            expected_access = self.access_records[access_id]

            self.assertEqual(serialized_access, expected_access)

    @tag("controllers.access.fetch_access_access_dne")
    def test_fetch_access_access_dne(self) -> None:
        """Fail Case: Fetch an `Access` record, given its id where
        that `Access` record does not exist."""

        admin = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_ADMIN_USER_EMAIL
        )

        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.fetch_accesses(
                access=arguments.FETCH_ACCESS_BY_ID_ACCESS_DNE,
                user=None,
                role_levels=None,
                subfunctions=None,
                include_revoked=None,
                admin=admin,
            )

    @tag("controllers.access.fetch_accesses_not_authenticated")
    def test_fetch_accesses_not_authenticated(self) -> None:
        """Fail Case: Fetch all `Access` records where the given
        admin is not authenticated."""

        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.fetch_accesses(
                access=None,
                user=None,
                role_levels=None,
                subfunctions=None,
                include_revoked=None,
                admin=cast(AuthModels.User, AuthModels.AnonymousUser()),
            )

    @tag("controllers.access.fetch_accesses_permissions_denied")
    def test_fetch_accesses_permissions_denied(self) -> None:
        """Fail Case: Fetch all `Access` record where the given admin
        does not have the appropriate permissions."""

        admin = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_NON_ADMIN_USER_EMAIL
        )

        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.fetch_accesses(
                access=None,
                user=None,
                role_levels=None,
                subfunctions=None,
                include_revoked=None,
                admin=admin,
            )
