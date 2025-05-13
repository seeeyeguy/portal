"""
Collection of pytests for Access's create controller.
"""

from typing import List

from django.test import tag

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

    fixtures: List[str] = []

    @tag("controllers.access.create_access")
    def test_create_access(self) -> None:
        """Success Case: Create an `Access` record."""

    @tag("controllers.access.create_access_user_dne")
    def test_create_access_user_dne(self) -> None:
        """Fail Case: Create an `Access` record where the `User`
        related to the given user email does not exist."""

    @tag("controllers.access.create_access_role_dne")
    def test_create_access_role_dne(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        related to the given role level does not exist."""

    @tag("controllers.access.create_access_subfunctions_dne")
    def test_create_access_subfunctions_dne(self) -> None:
        """Fail Case: Create an `Access` record where some of
        the given subfunctions do not exist."""

    @tag("controllers.access.create_access_stages_dne")
    def test_create_access_stages_dne(self) -> None:
        """Fail Case: Create an `Access` record where some of
        `Stage`s related to the given stage levels do not exist."""

    @tag("controllers.access.create_access_subfunctions_not_permitted")
    def test_create_access_subfunctions_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        is not permitted assigned `Subfunction`s"""

    @tag("controllers.access.create_access_stages_not_permitted")
    def test_create_access_stages_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        is not permitted assigned `Stage`s."""

    @tag("controllers.access.create_access_not_authenticated")
    def test_create_access_not_authenticated(self) -> None:
        """Fail Case: Create an `Access` record where the given
        admin is not authenticated."""

    @tag("controllers.access.create_access_permissions_denied")
    def test_create_access_permissions_denied(self) -> None:
        """Fail Case: Create an `Access` record where the given
        admin does not have the appropriate permissions."""
