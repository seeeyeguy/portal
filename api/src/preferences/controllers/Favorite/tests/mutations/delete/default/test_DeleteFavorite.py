"""
Collection of pytests for Favorite's delete controller.
"""

from typing import List

from django.test import tag, TestCase

from portal.models.fixtures import COMMON_FIXTURES


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

    fixtures: List[str] = [*COMMON_FIXTURES]

    @tag("controllers.favorite.delete_favorite")
    def test_delete_favorite(self) -> None:
        """Success Case: Delete `Favorite` record with given id."""
