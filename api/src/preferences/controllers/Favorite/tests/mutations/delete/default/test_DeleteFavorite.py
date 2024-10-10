"""
Collection of pytests for Favorite's delete controller.
"""

from typing import List

from django.test import tag, TestCase


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
        "portal/models/fixtures/employeelevels/employeelevels.json",
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
        "portal/models/fixtures/tags/tags.json",
        "portal/models/fixtures/stages/stages.json",
        "portal/models/fixtures/users/users.json",
        "portal/models/fixtures/roles/roles.json",
        "portal/models/fixtures/accesses/accesses.json",
    ]

    @tag("controllers.favorite.delete_favorite")
    def test_delete_favorite(self) -> None:
        """Success Case: Delete `Favorite` record with given id."""
