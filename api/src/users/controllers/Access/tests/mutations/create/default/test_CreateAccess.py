"""
Collection of pytests for Access's create controller.
"""

import pytest
from typing import cast, List

from django.contrib.auth import models as AuthModels
from django.test import tag

from users import controllers, exceptions, models
from users.controllers.Access.tests.mutations.create.default import arguments
from users.models.Access.serializers import AccessSerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "users",
    "access",
    "controllers.TestCreateAccess",
    "users.access.create",
    "access.create.default",
)
class TestCreateAccess(MultiDBTestCase):
    """Test suite for `Access`'s create controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "users/controllers/Access/tests/mutations/create/default/fixtures/users.json",
    ]

    @tag("controllers.access.create_access")
    def test_create_access(self) -> None:
        """Success Case: Create an `Access` record."""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )

        access = controllers.Access.create_access(
            user=arguments.CREATE_ACCESS_USER_EMAIL,
            role_level=arguments.CREATE_ACCESS_ROLE_LEVEL,
            subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
            stage_levels=arguments.CREATE_ACCESS_STAGE_LEVELS,
            admin=admin,
        )

        self.assertIsInstance(access, models.Access)
        self.assertIsNotNone(access.access_granted_date)

        data: dict = AccessSerializer(access).data
        del data["access_granted_date"]

        self.assertDictEqual(data, arguments.CREATE_ACCESS_EXPECTED_ACCESS)

    @tag("controller.access.create_access_already_exists")
    def test_create_access_already_exists(self) -> None:
        """Fail Case: Create an `Access` record where the
        `User` related to the given user email already has
        an active `Access` record related to the `Role` for the given
        role level."""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_ALREADY_EXISTS_USER_EMAIL,
                role_level=arguments.CREATE_ACCESS_ALREADY_EXISTS_ROLE_LEVEL,
                subfunctions=arguments.CREATE_ACCESS_ALREADY_EXISTS_SUBFUNCTION_IDS,
                stage_levels=[],
                admin=admin,
            )

    @tag("controllers.access.create_access_user_dne")
    def test_create_access_user_dne(self) -> None:
        """Fail Case: Create an `Access` record where the `User`
        related to the given user email does not exist."""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_USER_EMAIL_DNE,
                role_level=arguments.CREATE_ACCESS_ROLE_LEVEL,
                subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
                stage_levels=arguments.CREATE_ACCESS_STAGE_LEVELS,
                admin=admin,
            )

    @tag("controllers.access.create_access_role_dne")
    def test_create_access_role_dne(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        related to the given role level does not exist."""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_USER_EMAIL,
                role_level=arguments.CREATE_ACCESS_ROLE_LEVEL_DNE,
                subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
                stage_levels=arguments.CREATE_ACCESS_STAGE_LEVELS,
                admin=admin,
            )

    @tag("controllers.access.create_access_subfunctions_dne")
    def test_create_access_subfunctions_dne(self) -> None:
        """Fail Case: Create an `Access` record where some of
        the given subfunctions do not exist."""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_USER_EMAIL,
                role_level=arguments.CREATE_ACCESS_ROLE_LEVEL,
                subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS_DNE,
                stage_levels=arguments.CREATE_ACCESS_STAGE_LEVELS,
                admin=admin,
            )

    @tag("controllers.access.create_access_stages_dne")
    def test_create_access_stages_dne(self) -> None:
        """Fail Case: Create an `Access` record where some of
        `Stage`s related to the given stage levels do not exist."""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_USER_EMAIL,
                role_level=arguments.CREATE_ACCESS_ROLE_LEVEL,
                subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
                stage_levels=arguments.CREATE_ACCESS_STAGE_LEVELS_DNE,
                admin=admin,
            )

    @tag("controllers.access.create_access_subfunctions_not_permitted")
    def test_create_access_subfunctions_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        is not permitted assigned `Subfunction`s"""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_USER_EMAIL,
                role_level=arguments.CREATE_ACCESS_ROLE_NOT_PERMITTED_SUBFUNCTIONS_ROLE_LEVEL,
                subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
                stage_levels=arguments.CREATE_ACCESS_STAGE_LEVELS,
                admin=admin,
            )

    @tag("controllers.access.create_access_stages_not_permitted")
    def test_create_access_stages_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        is not permitted assigned `Stage`s."""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_USER_EMAIL,
                role_level=arguments.CREATE_ACCESS_ROLE_NOT_PERMITTED_STAGES_ROLE_LEVEL,
                subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
                stage_levels=arguments.CREATE_ACCESS_STAGE_LEVELS,
                admin=admin,
            )

    @tag("controllers.access.create_access_terminal_stages_not_permitted")
    def test_create_access_terminal_stages_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the given
        stage level belongs to a terminal `Stage`."""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_USER_EMAIL,
                role_level=arguments.CREATE_ACCESS_ROLE_LEVEL,
                subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
                stage_levels=arguments.CREATE_ACCESS_TERMINAL_STAGES_NOT_PERMITTED_STAGE_LEVELS,
                admin=admin,
            )

    @tag("controllers.access.create_access_draft_stage_not_permitted")
    def test_create_access_draft_stage_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the given
        stage level belongs to the `DRAFT` `Stage`."""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_USER_EMAIL,
                role_level=arguments.CREATE_ACCESS_ROLE_LEVEL,
                subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
                stage_levels=arguments.CREATE_ACCESS_DRAFT_STAGE_NOT_PERMITTED_STAGE_LEVELS,
                admin=admin,
            )

    @tag("controllers.access.create_access_invalid_stages_for_role")
    def test_create_access_invalid_stages_for_role(self) -> None:
        """Fail Case: Create an `Access` record where the given
        stage levels are not valid for the `Role`."""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_USER_EMAIL,
                role_level=arguments.CREATE_ACCESS_ROLE_LEVEL,
                subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
                stage_levels=arguments.CREATE_ACCESS_INVALID_STAGES_FOR_ROLE_STAGE_LEVELS,
                admin=admin,
            )

    @tag("controllers.access.create_access_not_authenticated")
    def test_create_access_not_authenticated(self) -> None:
        """Fail Case: Create an `Access` record where the given
        admin is not authenticated."""

        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_USER_EMAIL,
                role_level=arguments.CREATE_ACCESS_ROLE_LEVEL,
                subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
                stage_levels=arguments.CREATE_ACCESS_STAGE_LEVELS,
                admin=cast(AuthModels.User, AuthModels.AnonymousUser()),
            )

    @tag("controllers.access.create_access_permissions_denied")
    def test_create_access_permissions_denied(self) -> None:
        """Fail Case: Create an `Access` record where the given
        admin does not have the appropriate permissions."""

        admin = AuthModels.User.objects.get(
            email=arguments.CREATE_ACCESS_NON_ADMIN_USER_EMAIL
        )
        with pytest.raises(exceptions.UsersError):
            _ = controllers.Access.create_access(
                user=arguments.CREATE_ACCESS_USER_EMAIL,
                role_level=arguments.CREATE_ACCESS_ROLE_LEVEL,
                subfunctions=arguments.CREATE_ACCESS_SUBFUNCTION_IDS,
                stage_levels=arguments.CREATE_ACCESS_STAGE_LEVELS,
                admin=admin,
            )
