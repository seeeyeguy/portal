"""
Collection of pytests for Favorite's delete controller.
"""

import pytest
from typing import List

from django.test import tag, TestCase

from portal.models.fixtures import COMMON_FIXTURES
from preferences.controllers.Favorite.Favorite import Favorite
from preferences.controllers.Favorite.tests.mutations.delete.default import arguments
from preferences.exceptions import PreferencesError


@tag(
    "controllers",
    "preferences",
    "favorite",
    "controllers.TestDeleteFavorite",
    "preferences.favorite.delete",
    "favorite.delete.default",
)
class TestDeleteFavorite(TestCase):
    """Test suite for Favorite's delete controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/Favorite/tests/mutations/delete/default/fixtures/resources.json",
        "preferences/controllers/Favorite/tests/mutations/delete/default/fixtures/requests.json",
        "preferences/controllers/Favorite/tests/mutations/delete/default/fixtures/transitions.json",
        "preferences/controllers/Favorite/tests/mutations/delete/default/fixtures/dispositions.json",
        "preferences/controllers/Favorite/tests/mutations/delete/default/fixtures/favorites.json",
    ]

    @tag("controllers.favorite.delete_favorite")
    def test_delete_favorite(self) -> None:
        """Success Case: Delete `Favorite` record with given id."""

        rows_deleted = Favorite.delete_favorite(
            favorite_id=arguments.DELETE_FAVORITE_FAVORITE_ID
        )
        self.assertEqual(rows_deleted, arguments.DELETE_FAVORITE_DELETED_ROWS)

    @tag("controllers.favorite.delete_favorite_dne")
    def test_delete_favorite_dne(self) -> None:
        """Fail Case: Delete `Favorite` record when a Favorite
        does not exist for the given id."""

        with pytest.raises(PreferencesError):
            _ = Favorite.delete_favorite(
                favorite_id=arguments.DELETE_FAVORITE_FAVORITE_ID_DNE
            )
