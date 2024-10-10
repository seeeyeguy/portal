"""Collection of pytests for the Favorite's rank view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "preferences",
    "favorite",
    "views",
    "preferences.favorite.rank",
    "favorite.rank.default",
    "views.TestRankFavorite",
)
class TestRankFavorite(TestCase):
    """
    Tests for PUT /v1/preferences/favorites endpoint.
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

    @tag("views.favorite.rank_favorites")
    def test_rank_favorites(self) -> None:
        """Success Case: Rank a user's favorites."""

    @tag("views.favorite.rank_favorites_user_dne")
    def test_rank_favorites_user_dne(self) -> None:
        """Fail Case: Rank a user's favorites for a `User`
        that does not exist."""

    @tag("views.favorite.rank_favorites_resource_dne")
    def test_rank_favorites_resource_dne(self) -> None:
        """Fail Case: Rank a user's favorites where a `Resource`
        does not exist."""

    @tag("views.favorite.rank_favorites_duplicate_ranks")
    def test_rank_favorites_duplicate_ranks(self) -> None:
        """Fail Case: Rank a user's favorites where several favorites
        have a duplicate rank."""
