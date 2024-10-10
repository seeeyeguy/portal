"""Collection of pytests for the Favorite's delete view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse

from portal.models.fixtures import COMMON_FIXTURES


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

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("preferences.favorite")

    @tag("views.favorite.delete_favorite")
    def test_delete_favorite(self) -> None:
        """Success Case: Delete `Favorite` record with given id."""
