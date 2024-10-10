"""Collection of pytests for the Favorite's delete view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "preferences",
    "favorite",
    "views",
    "preferences.favorite.delete",
    "favorite.delete.default",
    "views.TestDeleteFavorite",
)
class TestDeleteFavorite(TestCase):
    """
    Tests for DELETE /v1/preferences/favorites endpoint.
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

    @tag("views.favorite.delete_favorite")
    def test_delete_favorite(self) -> None:
        """Success Case: Delete `Favorite` record with given id."""
