"""
Collection of pytests for Favorite's create controller.
"""

import pytest
from typing import List

from django.test import tag, TestCase

from portal.models.fixtures import COMMON_FIXTURES
from preferences import exceptions
from preferences.controllers import Favorite
from preferences.controllers.Favorite.tests.mutations.create.default import arguments
from preferences.models.Favorite import Favorite as FavoriteModel, serializers


@tag(
    "controllers",
    "preferences",
    "favorite",
    "controllers.TestCreateFavorite",
    "preferences.favorite.create",
    "favorite.create.default",
)
class TestCreateFavorite(TestCase):
    """Test suite for Favorite's create controller."""

    # pylint: disable=line-too-long
    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/Favorite/tests/mutations/create/default/fixtures/resources.json",
        "preferences/controllers/Favorite/tests/mutations/create/default/fixtures/requests.json",
        "preferences/controllers/Favorite/tests/mutations/create/default/fixtures/transitions.json",
        "preferences/controllers/Favorite/tests/mutations/create/default/fixtures/dispositions.json",
        "preferences/controllers/Favorite/tests/mutations/create/default/fixtures/favorites.json",
    ]

    @tag("controllers.favorite.create_favorite")
    def test_create_favorite(self) -> None:
        """Success Case: Create a `Favorite` record."""

        # Create `Favorite` record.
        favorite = Favorite.create_favorite(
            user=arguments.CREATE_FAVORITE_USER,
            resource=arguments.CREATE_FAVORITE_RESOURCE_ID,
        )

        self.assertIsInstance(favorite, FavoriteModel)

        # Serialize `Favorite`.
        serialized_favorite = serializers.FavoriteSerializer(favorite).data

        # Remove dynamic primary key and datetime fields before comparison.
        del serialized_favorite["id"]
        del serialized_favorite["created"]

        self.assertEqual(serialized_favorite, arguments.CREATE_FAVORITE_EXPECTED_VALUES)

    @tag("controllers.favorite.create_favorite_user_dne")
    def test_create_favorite_user_dne(self) -> None:
        """Fail Case: Create a `Favorite` record with a `User`
        that does not exist."""

        with pytest.raises(exceptions.PreferencesError):
            _ = Favorite.create_favorite(
                user=arguments.CREATE_FAVORITE_USER_DNE,
                resource=arguments.CREATE_FAVORITE_RESOURCE_ID,
            )

    @tag("controllers.favorite.create_favorite_resource_dne")
    def test_create_favorite_resource_dne(self) -> None:
        """Fail Case: Create a `Favorite` record with a given resource id
        where that `Resource` does not exist."""

        with pytest.raises(exceptions.PreferencesError):
            _ = Favorite.create_favorite(
                user=arguments.CREATE_FAVORITE_USER,
                resource=arguments.CREATE_FAVORITE_RESOURCE_DNE,
            )

    @tag("controllers.favorite.create_favorite_existing_favorite")
    def test_create_favorite_existing_favorite(self) -> None:
        """Fail Case: Create a `Favorite` record with a `Favorite` record that
        already exists for the given `User` and `Resource`."""

        with pytest.raises(exceptions.PreferencesError):
            _ = Favorite.create_favorite(
                user=arguments.CREATE_FAVORITE_USER,
                resource=arguments.CREATE_FAVORITE_EXISTING_FAVORITE_RESOURCE_ID,
            )

    @tag("controllers.favorite.create_favorite_inactive_resource")
    def test_create_favorite_inactive_resource(self) -> None:
        """Fail Case: Create a `Favorite` record with a given resource id
        where that `Resource` is inactive."""

        with pytest.raises(exceptions.PreferencesError):
            _ = Favorite.create_favorite(
                user=arguments.CREATE_FAVORITE_USER,
                resource=arguments.CREATE_FAVORITE_INACTIVE_RESOURCE_ID,
            )
