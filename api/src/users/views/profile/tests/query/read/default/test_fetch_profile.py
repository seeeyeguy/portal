"""
Collection of pytests for Profile's fetch view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


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

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
        "portal/models/fixtures/tags/tags.json",
        "portal/models/fixtures/stages/stages.json",
        "portal/models/fixtures/users/users.json",
        "portal/models/fixtures/roles/roles.json",
        "portal/models/fixtures/accesses/accesses.json",
    ]

    url: str = reverse("users.profile")

    @tag("views.profile.fetch_profile_by_user")
    def test_fetch_profile_by_user(self) -> None:
        """Success Case: Fetch `Profile` record for the
        given user."""

    @tag("views.profile.fetch_profile_by_user_dne")
    def test_fetch_profile_by_user_dne(self) -> None:
        """Fail Case: Fetch `Profile` record for a `User`
        that does not exist."""
