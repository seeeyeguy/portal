"""Collection of pytests for the Favorite's create view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


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
