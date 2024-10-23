"""
Collection of pytests for Profile's fetch view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from users.controllers.Profile.tests.query.read.default import arguments


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

    def setUp(self) -> None:
        super().setUp()
        user = AuthModels.User.objects.get(
            email__iexact=arguments.VALID_PROFILE_USER_EMAIL
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "users/controllers/Profile/tests/query/read/default/fixtures/profile.json",
    ]

    url: str = reverse("users.profile")

    @tag("views.profile.fetch_profile_by_user")
    def test_fetch_profile_by_user(self) -> None:
        """Success Case: Fetch `Profile` record for the
        given user."""

        request_url: str = f"{self.url}?user={arguments.VALID_PROFILE_USER_EMAIL}"
        response = self.client.get(request_url)

        profile = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(profile, dict)

        self.assertEqual(profile, arguments.VALID_PROFILE_DICTIONARY)

    @tag("views.profile.fetch_profile_by_user_permissions_denied")
    def test_fetch_profile_by_user_permissions_denied(self) -> None:
        """Fail Case: Fetch `Profile` record for the wrong `User`."""

        request_url: str = f"{self.url}?user={arguments.WRONG_VALID_PROFILE_USER_EMAIL}"
        response = self.client.get(request_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
