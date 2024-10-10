"""Collection of pytests for the Favorite's fetch view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


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

    url: str = reverse("preferences.favorite")

    @tag("views.favorite.fetch_favorites_by_user")
    def test_fetch_favorites_by_user(self) -> None:
        """Success Case: Fetch all `Favorite` records for
        the given user."""

    @tag("views.favorite.fetch_favorites_by_user_dne")
    def test_fetch_favorites_by_user_dne(self) -> None:
        """Fail Case: Fetch all `Favorite` records for
        a `User` that does not exist."""
