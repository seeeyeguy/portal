"""
Collection of pytests for Access's fetch view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from users import models
from users.controllers.Access.tests.query.read.default import arguments
from users.models.Access.serializers import AccessSerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "users",
    "access",
    "views",
    "users.access.fetch",
    "access.fetch.default",
    "views.TestFetchAccess",
)
class TestFetchAccess(MultiDBTestCase):
    """
    Tests for GET /v1/users/access endpoint.
    """

    def setUp(self) -> None:

        super().setUp()

        user = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_ADMIN_USER_EMAIL
        )
        self.client.force_login(user=user)

        self.access_records = {}
        for access_id in arguments.FETCH_ACCESSES_ALL_ACCESS_ACCESS_IDS:
            serialized_access = AccessSerializer(
                models.Access.objects.get(id=access_id)
            ).data
            self.access_records[access_id] = serialized_access

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "users/controllers/Access/tests/query/read/default/fixtures/users.json",
        "users/controllers/Access/tests/query/read/default/fixtures/accesses.json",
    ]

    url: str = reverse("users.access")

    @tag("views.access.fetch_access")
    def test_fetch_access(self) -> None:
        """Success Case: Fetch an `Access` record, given its id."""

        access_params: dict = {"id": arguments.FETCH_ACCESS_BY_ID_ACCESS_ID}

        response = self.client.get(
            self.url, access_params, headers={"content_type": "application/json"}
        )

        access = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(access, dict)

        self.assertEqual(
            access, self.access_records[arguments.FETCH_ACCESS_BY_ID_ACCESS_ID]
        )

    @tag("views.access.fetch_accesses")
    def test_fetch_accesses(self) -> None:
        """Success Case: Fetch all `Access` records."""

        response = self.client.get(
            self.url, headers={"content_type": "application/json"}
        )

        accesses = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(accesses, list)

        self.assertEqual(
            len(accesses),
            len(arguments.FETCH_ACCESSES_VALID_ACCESS_RECORD_IDS),
        )

        for access in accesses:
            self.assertIsInstance(access, dict)

            access_id: int = access["id"]

            self.assertIn(access_id, arguments.FETCH_ACCESSES_VALID_ACCESS_RECORD_IDS)

            expected_access = self.access_records[access_id]

            self.assertEqual(access, expected_access)

    @tag("views.access.fetch_user_accesses")
    def test_fetch_user_accesses(self) -> None:
        """Success Case: Fetch all `Access` records for a `User`."""

        access_params: dict = {"user": arguments.FETCH_ACCESSES_BY_USER_USER_EMAIL}

        response = self.client.get(
            self.url, access_params, headers={"content_type": "application/json"}
        )

        accesses = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(accesses, list)

        self.assertEqual(
            len(accesses),
            len(arguments.FETCH_ACCESSES_FOR_USER_ACCESS_RECORD_IDS),
        )

        for access in accesses:
            self.assertIsInstance(access, dict)

            access_id: int = access["id"]

            self.assertIn(
                access_id, arguments.FETCH_ACCESSES_FOR_USER_ACCESS_RECORD_IDS
            )

            expected_access = self.access_records[access_id]

            self.assertEqual(access, expected_access)

    @tag("views.access.fetch_roles_accesses")
    def test_fetch_roles_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s."""

        access_params: dict = {
            "role_levels": arguments.FETCH_ACCESSES_WITH_ROLE_LEVELS_ROLE_LEVELS
        }

        response = self.client.get(
            self.url, access_params, headers={"content_type": "application/json"}
        )

        accesses = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(accesses, list)

        self.assertEqual(
            len(accesses),
            len(arguments.FETCH_ACCESSES_FOR_ROLE_LEVELS_ACCESS_RECORD_IDS),
        )

        for access in accesses:
            self.assertIsInstance(access, dict)

            access_id: int = access["id"]

            self.assertIn(
                access_id, arguments.FETCH_ACCESSES_FOR_ROLE_LEVELS_ACCESS_RECORD_IDS
            )

            expected_access = self.access_records[access_id]

            self.assertEqual(access, expected_access)

    @tag("views.access.fetch_subfunctions_accesses")
    def test_fetch_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `SubFunction`s."""

        access_params: dict = {
            "subfunctions": arguments.FETCH_ACCESSES_WITH_SUBFUNCTIONS_SUBFUNCTIONS
        }

        response = self.client.get(
            self.url, access_params, headers={"content_type": "application/json"}
        )

        accesses = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(accesses, list)

        self.assertEqual(
            len(accesses),
            len(arguments.FETCH_ACCESSES_FOR_SUBFUNCTIONS_ACCESS_RECORD_IDS),
        )

        for access in accesses:
            self.assertIsInstance(access, dict)

            access_id: int = access["id"]

            self.assertIn(
                access_id, arguments.FETCH_ACCESSES_FOR_SUBFUNCTIONS_ACCESS_RECORD_IDS
            )

            expected_access = self.access_records[access_id]

            self.assertEqual(access, expected_access)

    @tag("views.access.fetch_user_roles_accesses")
    def test_fetch_user_roles_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s for a `User`."""

        access_params: dict = {
            "user": arguments.FETCH_ACCESSES_WITH_USER_AND_ROLES_USER_EMAIL,
            "role_levels": arguments.FETCH_ACCESSES_WITH_USER_AND_ROLE_LEVELS_ROLE_LEVELS,
        }

        response = self.client.get(
            self.url, access_params, headers={"content_type": "application/json"}
        )

        accesses = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(accesses, list)

        self.assertEqual(
            len(accesses),
            len(arguments.FETCH_ACCESSES_WITH_USER_AND_ROLE_LEVELS_ACCESS_RECORD_IDS),
        )

        for access in accesses:
            self.assertIsInstance(access, dict)

            access_id: int = access["id"]

            self.assertIn(
                access_id,
                arguments.FETCH_ACCESSES_WITH_USER_AND_ROLE_LEVELS_ACCESS_RECORD_IDS,
            )

            expected_access = self.access_records[access_id]

            self.assertEqual(access, expected_access)

    @tag("views.access.fetch_user_subfunctions_accesses")
    def test_fetch_user_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `SubFunction`s for a `User`."""

        access_params: dict = {
            "user": arguments.FETCH_ACCESSES_WITH_USER_AND_SUBFUNCTIONS_USER_EMAIL,
            "subfunctions": arguments.FETCH_ACCESSES_WITH_USER_AND_SUBFUNCTIONS_SUBFUNCTIONS,
        }

        response = self.client.get(
            self.url, access_params, headers={"content_type": "application/json"}
        )

        accesses = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(accesses, list)

        self.assertEqual(
            len(accesses),
            len(arguments.FETCH_ACCESSES_WITH_USER_AND_SUBFUNCTIONS_ACCESS_RECORD_IDS),
        )

        for access in accesses:
            self.assertIsInstance(access, dict)

            access_id: int = access["id"]

            self.assertIn(
                access_id,
                arguments.FETCH_ACCESSES_WITH_USER_AND_SUBFUNCTIONS_ACCESS_RECORD_IDS,
            )

            expected_access = self.access_records[access_id]

            self.assertEqual(access, expected_access)

    @tag("views.access.fetch_user_roles_subfunctions_accesses")
    def test_fetch_user_roles_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s and `SubFunction`s for a `User`."""

        access_params: dict = {
            "user": arguments.FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_USER_EMAIL,
            "role_levels": arguments.FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_ROLE_LEVELS,
            "subfunctions": arguments.FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_SUBFUNCTIONS,
        }

        response = self.client.get(
            self.url, access_params, headers={"content_type": "application/json"}
        )

        accesses = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(accesses, list)

        self.assertEqual(
            len(accesses),
            len(
                arguments.FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_ACCESS_RECORD_IDS
            ),
        )

        for access in accesses:
            self.assertIsInstance(access, dict)

            access_id: int = access["id"]

            self.assertIn(
                access_id,
                arguments.FETCH_ACCESSES_WITH_USER_ROLE_LEVELS_AND_SUBFUNCTIONS_ACCESS_RECORD_IDS,
            )

            expected_access = self.access_records[access_id]

            self.assertEqual(access, expected_access)

    @tag("views.access.fetch_accesses_include_revoked")
    def test_fetch_accesses_include_revoked(self) -> None:
        """Success Case: Fetch all `Access` records, including
        revoked `Access` records."""

        access_params: dict = {"include_revoked": True}

        response = self.client.get(
            self.url, access_params, headers={"content_type": "application/json"}
        )

        accesses = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(accesses, list)

        self.assertEqual(
            len(accesses),
            len(arguments.FETCH_ACCESSES_ALL_ACCESS_ACCESS_IDS),
        )

        for access in accesses:
            self.assertIsInstance(access, dict)

            access_id: int = access["id"]

            self.assertIn(
                access_id,
                arguments.FETCH_ACCESSES_ALL_ACCESS_ACCESS_IDS,
            )

            expected_access = self.access_records[access_id]

            self.assertEqual(access, expected_access)

    @tag("views.access.fetch_access_access_dne")
    def test_fetch_access_access_dne(self) -> None:
        """Fail Case: Fetch an `Access` record, given its id where
        that `Access` record does not exist."""

        access_params: dict = {"id": arguments.FETCH_ACCESS_BY_ID_ACCESS_DNE}

        response = self.client.get(
            self.url, access_params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.access.fetch_access_permissions_denied")
    def test_fetch_access_permissions_denied(self) -> None:
        """Fail Case: Fetch all `Access` records, where
        request.`User` does not have the appropriate permissions."""

        user = AuthModels.User.objects.get(
            username=arguments.FETCH_ACCESSES_NON_ADMIN_USER_EMAIL
        )
        self.client.force_login(user=user)

        response = self.client.get(
            self.url, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
