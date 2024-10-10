"""Collection of pytests for the Favorite's fetch view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "preferences",
    "favorite",
    "views",
    "preferences.favorite.fetch",
    "favorite.fetch.default",
    "views.TestFetchFavorite",
)
class TestFetchFavorite(TestCase):
    """
    Tests for GET /v1/preferences/favorites endpoint.
    """

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("preferences.favorite")

    @tag("views.favorite.fetch_favorites_by_user")
    def test_fetch_favorites_by_user(self) -> None:
        """Success Case: Fetch all `Favorite` records for
        the given user."""

    @tag("views.favorite.fetch_favorites_by_user_dne")
    def test_fetch_favorites_by_user_dne(self) -> None:
        """Fail Case: Fetch all `Favorite` records for
        a `User` that does not exist."""
