"""
Collection of pytests for Access's create view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from users.controllers.Access.tests.mutations.create.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "user",
    "access",
    "views",
    "users.access.create",
    "access.create.default",
    "views.TestCreateAccess",
)
class TestCreateAccess(MultiDBTestCase):
    """
    Tests for POST /v1/users/access endpoint.
    """

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "users/controllers/Access/tests/mutations/create/default/fixtures/users.json",
    ]

    url: str = reverse("users.access")

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            username=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )
        self.client.force_login(user=user)

    @tag("views.access.create_access")
    def test_create_access(self) -> None:
        """Success Case: Create an `Access` record."""

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL,
            "role_level": arguments.CREATE_ACCESS_ROLE_LEVEL,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            "stage_levels": arguments.CREATE_ACCESS_STAGE_LEVELS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        access = response.json()
        del access["access_granted_date"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertDictEqual(access, arguments.CREATE_ACCESS_EXPECTED_ACCESS)

    @tag("views.access.create_access_user_dne")
    def test_create_access_user_dne(self) -> None:
        """Fail Case: Create an `Access` record where the `User`
        related to the given user email does not exist."""

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL_DNE,
            "role_level": arguments.CREATE_ACCESS_ROLE_LEVEL,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            "stage_levels": arguments.CREATE_ACCESS_STAGE_LEVELS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.access.create_access_role_dne")
    def test_create_access_role_dne(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        related to the given role level does not exist."""

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL,
            "role_level": arguments.CREATE_ACCESS_ROLE_LEVEL_DNE,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            "stage_levels": arguments.CREATE_ACCESS_STAGE_LEVELS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.access.create_access_subfunctions_dne")
    def test_create_access_subfunctions_dne(self) -> None:
        """Fail Case: Create an `Access` record where some of
        the given subfunctions do not exist."""

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL,
            "role_level": arguments.CREATE_ACCESS_ROLE_LEVEL,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS_DNE,
            "stage_levels": arguments.CREATE_ACCESS_STAGE_LEVELS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.access.create_access_stages_dne")
    def test_create_access_stages_dne(self) -> None:
        """Fail Case: Create an `Access` record where some of
        `Stage`s related to the given stage levels do not exist."""

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL,
            "role_level": arguments.CREATE_ACCESS_ROLE_LEVEL,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            "stage_levels": arguments.CREATE_ACCESS_STAGE_LEVELS_DNE,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.access.create_access_subfunctions_not_permitted")
    def test_create_access_subfunctions_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        is not permitted assigned `Subfunction`s"""

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL,
            "role_level": arguments.CREATE_ACCESS_ROLE_NOT_PERMITTED_SUBFUNCTIONS_ROLE_LEVEL,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            "stage_levels": arguments.CREATE_ACCESS_STAGE_LEVELS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.access.create_access_stages_not_permitted")
    def test_create_access_stages_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        is not permitted assigned `Stage`s."""

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL,
            "role_level": arguments.CREATE_ACCESS_ROLE_NOT_PERMITTED_STAGES_ROLE_LEVEL,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            "stage_levels": arguments.CREATE_ACCESS_STAGE_LEVELS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.access.create_access_terminal_stages_not_permitted")
    def test_create_access_terminal_stages_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the given
        stage level belongs to a terminal `Stage`."""

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL,
            "role_level": arguments.CREATE_ACCESS_ROLE_LEVEL,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            "stage_levels": arguments.CREATE_ACCESS_TERMINAL_STAGES_NOT_PERMITTED_STAGE_LEVELS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.access.create_access_draft_stage_not_permitted")
    def test_create_access_draft_stage_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the given
        stage level belongs to the `DRAFT` `Stage`."""

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL,
            "role_level": arguments.CREATE_ACCESS_ROLE_LEVEL,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            "stage_levels": arguments.CREATE_ACCESS_DRAFT_STAGE_NOT_PERMITTED_STAGE_LEVELS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.access.create_access_invalid_stages_for_role")
    def test_create_access_invalid_stages_for_role(self) -> None:
        """Fail Case: Create an `Access` record where the given
        stage levels are not valid for the `Role`."""

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL,
            "role_level": arguments.CREATE_ACCESS_ROLE_LEVEL,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            "stage_levels": arguments.CREATE_ACCESS_INVALID_STAGES_FOR_ROLE_STAGE_LEVELS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.access.create_access_permissions_denied")
    def test_create_access_permissions_denied(self) -> None:
        """Fail Case: Create an `Access` record where the request `User`
        does not have the appropriate permissions."""

        user = AuthModels.User.objects.get(
            username=arguments.CREATE_ACCESS_NON_ADMIN_USER_EMAIL
        )

        self.client.force_login(user=user)

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL,
            "role_level": arguments.CREATE_ACCESS_ROLE_LEVEL,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            "stage_levels": arguments.CREATE_ACCESS_STAGE_LEVELS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("views.access.create_access_not_authenticated")
    def test_create_access_not_authenticated(self) -> None:
        """Fail Case: Create an `Access` record where the given
        admin is not authenticated."""

        self.client.logout()

        body: dict = {
            "user": arguments.CREATE_ACCESS_USER_EMAIL,
            "role_level": arguments.CREATE_ACCESS_ROLE_LEVEL,
            "subfunctions": arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            "stage_levels": arguments.CREATE_ACCESS_STAGE_LEVELS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
