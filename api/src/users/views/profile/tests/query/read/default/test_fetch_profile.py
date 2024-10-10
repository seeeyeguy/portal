"""
Collection of pytests for Profile's fetch view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "users",
    "profile",
    "views",
    "users.profile.fetch",
    "profile.fetch.default",
    "views.TestFetchProfile",
)
class TestFetchProfile(TestCase):
    """
    Tests for GET /v1/users/profile endpoint.
    """

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("users.profile")

    @tag("views.profile.fetch_profile_by_user")
    def test_fetch_profile_by_user(self) -> None:
        """Success Case: Fetch `Profile` record for the
        given user."""

    @tag("views.profile.fetch_profile_by_user_dne")
    def test_fetch_profile_by_user_dne(self) -> None:
        """Fail Case: Fetch `Profile` record for a `User`
        that does not exist."""
