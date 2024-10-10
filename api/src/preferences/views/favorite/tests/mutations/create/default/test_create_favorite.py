"""Collection of pytests for the Favorite's create view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "preferences",
    "favorite",
    "views",
    "preferences.favorite.create",
    "favorite.create.default",
    "views.TestCreateFavorite",
)
class TestCreateFavorite(TestCase):
    """
    Tests for POST /v1/preferences/favorites endpoint.
    """

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("preferences.favorite")

    @tag("views.favorite.create_favorite")
    def test_create_favorite(self) -> None:
        """Success Case: Create a `Favorite` record."""

    @tag("views.favorite.create_favorite_user_dne")
    def test_create_favorite_user_dne(self) -> None:
        """Fail Case: Create a `Favorite` record with a `User`
        that does not exist."""

    @tag("views.favorite.create_favorite_resource_dne")
    def test_create_favorite_resource_dne(self) -> None:
        """Fail Case: Create a `Favorite` record with a given resource id
        where that `Resource` does not exist."""
