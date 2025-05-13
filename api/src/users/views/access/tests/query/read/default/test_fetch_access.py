"""
Collection of pytests for Access's fetch view endpoint.
"""

from typing import List

# NEED TO REMOVE pylint-disable AFTER IMPLEMENTATION.
# pylint: disable=useless-parent-delegation
from django.test import tag
from django.urls import reverse

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

    fixtures: List[str] = []

    url: str = reverse("users.access")

    @tag("views.access.fetch_access")
    def test_fetch_access(self) -> None:
        """Success Case: Fetch an `Access` record, given its id."""

    @tag("views.access.fetch_accesses")
    def test_fetch_accesses(self) -> None:
        """Success Case: Fetch all `Access` records."""

    @tag("views.access.fetch_user_accesses")
    def test_fetch_user_accesses(self) -> None:
        """Success Case: Fetch all `Access` records for a `User`."""

    @tag("views.access.fetch_roles_accesses")
    def test_fetch_roles_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s."""

    @tag("views.access.fetch_subfunctions_accesses")
    def test_fetch_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `SubFunction`s."""

    @tag("views.access.fetch_user_roles_accesses")
    def test_fetch_user_roles_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s for a `User`."""

    @tag("views.access.fetch_user_subfunctions_accesses")
    def test_fetch_user_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `SubFunction`s for a `User`."""

    @tag("views.access.fetch_user_roles_subfunctions_accesses")
    def test_fetch_user_roles_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s and `SubFunction`s for a `User`."""

    @tag("views.access.fetch_accesses_include_revoked")
    def test_fetch_accesses_include_revoked(self) -> None:
        """Success Case: Fetch all `Access` records, including
        revoked `Access` records."""

    @tag("views.access.fetch_access_access_dne")
    def test_fetch_access_access_dne(self) -> None:
        """Fail Case: Fetch an `Access` record, given its id where
        that `Access` record does not exist."""

    @tag("views.access.fetch_access_permissions_denied")
    def test_fetch_access_permissions_denied(self) -> None:
        """Fail Case: Fetch all `Access` records, where
        request.`User` does not have the appropriate permissions."""
