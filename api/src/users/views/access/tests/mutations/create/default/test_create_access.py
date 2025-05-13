"""
Collection of pytests for Access's create view endpoint.
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
    "users.access.create",
    "access.create.default",
    "views.TestCreateAccess",
)
class TestCreateAccess(MultiDBTestCase):
    """
    Tests for POST /v1/users/access endpoint.
    """

    fixtures: List[str] = []

    url: str = reverse("users.access")

    def setUp(self) -> None:

        super().setUp()

    @tag("views.access.create_access")
    def test_create_access(self) -> None:
        """Success Case: Create an `Access` record."""

    @tag("views.access.create_access_user_dne")
    def test_create_access_user_dne(self) -> None:
        """Fail Case: Create an `Access` record where the `User`
        related to the given user email does not exist."""

    @tag("views.access.create_access_role_dne")
    def test_create_access_role_dne(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        related to the given role level does not exist."""

    @tag("views.access.create_access_subfunctions_dne")
    def test_create_access_subfunctions_dne(self) -> None:
        """Fail Case: Create an `Access` record where some of
        the given subfunctions do not exist."""

    @tag("views.access.create_access_stages_dne")
    def test_create_access_stages_dne(self) -> None:
        """Fail Case: Create an `Access` record where some of
        `Stage`s related to the given stage levels do not exist."""

    @tag("views.access.create_access_subfunctions_not_permitted")
    def test_create_access_subfunctions_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        is not permitted assigned `Subfunction`s"""

    @tag("views.access.create_access_stages_not_permitted")
    def test_create_access_stages_not_permitted(self) -> None:
        """Fail Case: Create an `Access` record where the `Role`
        is not permitted assigned `Stage`s."""

    @tag("views.access.create_access_permissions_denied")
    def test_create_access_permissions_denied(self) -> None:
        """Fail Case: Create an `Access` record where the request.`User`
        does not have the appropriate permissions."""
