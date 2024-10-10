"""
Collection of pytests for Favorite's fetch controller.
"""

from typing import List

from django.test import tag, TestCase

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "controllers",
    "preferences",
    "favorite",
    "controllers.TestFetchFavorite",
    "preferences.favorite.fetch",
    "favorite.fetch.default",
)
class TestFetchFavorite(TestCase):
    """Test suite for Favorite's fetch controller."""

    fixtures: List[str] = [*COMMON_FIXTURES]

    @tag("controllers.favorite.fetch_favorites_by_user")
    def test_fetch_favorites_by_user(self) -> None:
        """Success Case: Fetch all `Favorite` records for
        the given user."""

    @tag("controllers.favorite.fetch_favorites_by_user_dne")
    def test_fetch_favorites_by_user_dne(self) -> None:
        """Fail Case: Fetch all `Favorite` records for
        a `User` that does not exist."""
