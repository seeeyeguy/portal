"""
Collection of pytests for Favorite's rank controller.
"""

from typing import List

from django.test import tag, TestCase

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "controllers",
    "preferences",
    "favorite",
    "controllers.TestRankFavorite",
    "preferences.favorite.rank",
    "favorite.rank.default",
)
class TestRankFavorite(TestCase):
    """Test suite for Favorite's rank controller."""

    fixtures: List[str] = [*COMMON_FIXTURES]

    @tag("controllers.favorite.rank_favorites")
    def test_rank_favorites(self) -> None:
        """Success Case: Rank a user's favorites."""

    @tag("controllers.favorite.rank_favorites_user_dne")
    def test_rank_favorites_user_dne(self) -> None:
        """Fail Case: Rank a user's favorites for a `User`
        that does not exist."""

    @tag("controllers.favorite.rank_favorites_resource_dne")
    def test_rank_favorites_resource_dne(self) -> None:
        """Fail Case: Rank a user's favorites where a `Resource`
        does not exist."""

    @tag("controllers.favorite.rank_favorites_duplicate_ranks")
    def test_rank_favorites_duplicate_ranks(self) -> None:
        """Fail Case: Rank a user's favorites where several favorites
        have a duplicate rank."""
