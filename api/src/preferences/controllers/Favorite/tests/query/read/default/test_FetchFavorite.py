"""
Collection of pytests for Favorite's fetch controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import pytest
from typing import List

from django.db.models import QuerySet
from django.test import tag

from preferences.controllers.Favorite.Favorite import Favorite
from preferences.controllers.Favorite.tests.query.read.default import arguments
from preferences.exceptions import PreferencesError
from preferences.models.Favorite.Favorite import Favorite as FavoriteModel
from preferences.models.Favorite.serializers import FavoriteSerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "preferences",
    "favorite",
    "controllers.TestFetchFavorite",
    "preferences.favorite.fetch",
    "favorite.fetch.default",
)
class TestFetchFavorite(MultiDBTestCase):
    """Test suite for Favorite's fetch controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/resources.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/requests.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/transitions.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/dispositions.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/favorites.json",
    ]

    @tag("controllers.favorite.fetch_favorites_by_user")
    def test_fetch_favorites_by_user(self) -> None:
        """Success Case: Fetch all `Favorite` records for
        the given user."""

        favorites = Favorite.fetch_favorites(user=arguments.FETCH_FAVORITE_USER_EMAIL)

        self.assertIsInstance(favorites, QuerySet[FavoriteModel])

        # Serialize `Favorite` instances.
        serialized_favorites: List[dict] = FavoriteSerializer(favorites, many=True).data

        self.assertListEqual(serialized_favorites, arguments.VALID_FAVORITES)

    @tag("controllers.favorite.fetch_favorites_by_user_dne")
    def test_fetch_favorites_by_user_dne(self) -> None:
        """Fail Case: Fetch all `Favorite` records for
        a `User` that does not exist."""

        with pytest.raises(PreferencesError):
            _ = Favorite.fetch_favorites(user=arguments.FETCH_FAVORITE_USER_EMAIL_DNE)
