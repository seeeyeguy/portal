"""
Collection of pytests for Profile's fetch controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "users",
    "profile",
    "controllers.TestFetchProfile",
    "users.profile.fetch",
    "profile.fetch.default",
)
class TestFetchProfile(TestCase):
    """Test suite for Profile's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/users/users.json",
    ]

    @tag("controllers.profile.fetch_profile_by_user")
    def test_fetch_profile_by_user(self) -> None:
        """Success Case: Fetch `Profile` record for the
        given user."""

    @tag("controllers.profile.fetch_profile_by_user_dne")
    def test_fetch_profile_by_user_dne(self) -> None:
        """Fail Case: Fetch `Profile` record for a `User`
        that does not exist."""
