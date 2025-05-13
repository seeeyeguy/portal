"""
Collection of pytests for Access's fetch controller.
"""

from typing import List

from django.test import tag

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

    fixtures: List[str] = []

    @tag("controllers.access.fetch_access")
    def test_fetch_access(self) -> None:
        """Success Case: Fetch an `Access` record, given its id."""

    @tag("controllers.access.fetch_accesses")
    def test_fetch_accesses(self) -> None:
        """Success Case: Fetch all `Access` records."""

    @tag("controllers.access.fetch_user_accesses")
    def test_fetch_user_accesses(self) -> None:
        """Success Case: Fetch all `Access` records for a `User`."""

    @tag("controllers.access.fetch_roles_accesses")
    def test_fetch_roles_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s."""

    @tag("controllers.access.fetch_subfunctions_accesses")
    def test_fetch_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `SubFunction`s."""

    @tag("controllers.access.fetch_user_roles_accesses")
    def test_fetch_user_roles_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s for a `User`."""

    @tag("controllers.access.fetch_user_subfunctions_accesses")
    def test_fetch_user_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `SubFunction`s for a `User`."""

    @tag("controllers.access.fetch_user_roles_subfunctions_accesses")
    def test_fetch_user_roles_subfunctions_accesses(self) -> None:
        """Success Case: Fetch all `Access` records related to a
        set of `Role`s and `SubFunction`s for a `User`."""

    @tag("controllers.access.fetch_accesses_include_revoked")
    def test_fetch_accesses_include_revoked(self) -> None:
        """Success Case: Fetch all `Access` records, including
        revoked `Access` records."""

    @tag("controllers.access.fetch_access_access_dne")
    def test_fetch_access_access_dne(self) -> None:
        """Fail Case: Fetch an `Access` record, given its id where
        that `Access` record does not exist."""

    @tag("controllers.access.fetch_accesses_not_authenticated")
    def test_fetch_accesses_not_authenticated(self) -> None:
        """Fail Case: Fetch all `Access` records where the given
        admin is not authenticated."""

    @tag("controllers.access.fetch_accesses_permissions_denied")
    def test_fetch_accesses_permissions_denied(self) -> None:
        """Fail Case: Fetch all `Access` record where the given admin
        does not have the appropriate permissions."""
