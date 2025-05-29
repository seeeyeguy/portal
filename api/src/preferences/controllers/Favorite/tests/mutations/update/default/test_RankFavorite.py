"""
Collection of pytests for Favorite's rank controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import pytest
from typing import List

from django.db.models import QuerySet
from django.test import tag

from portal.models.fixtures import COMMON_FIXTURES
from preferences.controllers.Favorite.Favorite import Favorite
from preferences.controllers.Favorite.tests.mutations.update.default import arguments
from preferences.exceptions import PreferencesError
from preferences.models.Favorite.Favorite import Favorite as FavoriteModel
from preferences.models.Favorite.serializers import FavoriteSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "preferences",
    "favorite",
    "controllers.TestRankFavorite",
    "preferences.favorite.rank",
    "favorite.rank.default",
)
class TestRankFavorite(MultiDBTestCase):
    """Test suite for Favorite's rank controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/Favorite/tests/mutations/update/default/fixtures/resources.json",
        "preferences/controllers/Favorite/tests/mutations/update/default/fixtures/pointofcontacts.json",
        "preferences/controllers/Favorite/tests/mutations/update/default/fixtures/requests.json",
        "preferences/controllers/Favorite/tests/mutations/update/default/fixtures/transitions.json",
        "preferences/controllers/Favorite/tests/mutations/update/default/fixtures/dispositions.json",
        "preferences/controllers/Favorite/tests/mutations/update/default/fixtures/favorites.json",
    ]

    @tag("controllers.favorite.rank_favorites")
    def test_rank_favorites(self) -> None:
        """Success Case: Rank a user's favorites."""

        ranked_favorites = Favorite.rank_favorites(
            user=arguments.RANK_FAVORITE_USER_EMAIL,
            ranked_favorites=arguments.RANK_FAVORITE_RANKED_FAVORITES_PARAM,
        )

        self.assertIsInstance(ranked_favorites, QuerySet[FavoriteModel])

        # Serialize `Favorite` instances.
        serialized_favorites: List[dict] = FavoriteSerializer(
            ranked_favorites, many=True
        ).data

        self.assertListEqual(serialized_favorites, arguments.VALID_RANKED_FAVORITES)

    @tag("controllers.favorite.rank_favorites_user_dne")
    def test_rank_favorites_user_dne(self) -> None:
        """Fail Case: Rank a user's favorites for a `User`
        that does not exist."""

        with pytest.raises(PreferencesError):
            _ = Favorite.rank_favorites(
                user=arguments.RANK_FAVORITE_USER_EMAIL_DNE,
                ranked_favorites=arguments.RANK_FAVORITE_RANKED_FAVORITES_PARAM,
            )

    @tag("controllers.favorite.rank_favorites_favorite_dne")
    def test_rank_favorites_favorite_dne(self) -> None:
        """Fail Case: Rank a user's favorites where a `Favorite`
        does not exist for the user."""

        with pytest.raises(PreferencesError):
            _ = Favorite.rank_favorites(
                user=arguments.RANK_FAVORITE_USER_EMAIL,
                ranked_favorites=arguments.RANK_FAVORITE_RANKED_FAVORITES_PARAM_FAVORITE_DNE,
            )

    @tag("controllers.favorite.rank_favorites_mismatch_ranks")
    def test_rank_favorites_mismatch_ranks(self) -> None:
        """Fail Case: Rank a user's favorites where there is
        a mismatch between the existing ranks and the ones
        being supplied in the update."""

        with pytest.raises(PreferencesError):
            _ = Favorite.rank_favorites(
                user=arguments.RANK_FAVORITE_USER_EMAIL,
                ranked_favorites=arguments.RANK_FAVORITE_RANKED_FAVORITES_PARAM_MISMATCH_RANKS,
            )

    @tag("controllers.favorite.rank_favorites_duplicate_ranks")
    def test_rank_favorites_duplicate_ranks(self) -> None:
        """Fail Case: Rank a user's favorites where several favorites
        have a duplicate rank."""

        with pytest.raises(PreferencesError):
            _ = Favorite.rank_favorites(
                user=arguments.RANK_FAVORITE_USER_EMAIL,
                ranked_favorites=arguments.RANK_FAVORITE_RANKED_FAVORITES_PARAM_DUPLICATE_RANK,
            )
