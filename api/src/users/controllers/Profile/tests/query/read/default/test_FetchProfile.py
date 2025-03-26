"""
Collection of pytests for Profile's fetch controller.
"""

# pylint: disable=wrong-import-order
import pytest
from typing import List

from django.test import tag

from users import models
from users.controllers import Profile
from users.controllers.Profile.tests.query.read.default import arguments
from users.exceptions import UsersError
from users.models.Profile.serializers import ProfileSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "users",
    "profile",
    "controllers.TestFetchProfile",
    "users.profile.fetch",
    "profile.fetch.default",
)
class TestFetchProfile(MultiDBTestCase):
    """Test suite for Profile's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "users/controllers/Profile/tests/query/read/default/fixtures/profile.json",
    ]

    @tag("controllers.profile.fetch_profile_by_user")
    def test_fetch_profile_by_user(self) -> None:
        """Success Case: Fetch `Profile` record for the
        given user."""

        # Fetch `Profile` for user.
        profile = Profile.fetch_profile(user=arguments.VALID_PROFILE_USER_EMAIL)

        self.assertIsInstance(profile, models.Profile)
        self.assertEqual(
            ProfileSerializer(profile).data, arguments.VALID_PROFILE_DICTIONARY
        )

    @tag("controllers.profile.fetch_profile_by_user_dne")
    def test_fetch_profile_by_user_dne(self) -> None:
        """Fail Case: Fetch `Profile` record for a `User`
        that does not exist."""

        with pytest.raises(UsersError):
            _ = Profile.fetch_profile(user=arguments.INVALID_PROFILE_USER_EMAIL)
