"""
Collection of pytests for Favorite's fetch controller.
"""

import pytest
from typing import Any, List, cast

from django.db.models import QuerySet
from django.test import tag

from analytics.exceptions import AnalyticsError
from manager.utils.tests import MultiDBTestCase
from portal.models.fixtures import COMMON_FIXTURES
from preferences.controllers.Favorite.Favorite import Favorite
from preferences.controllers.Favorite.tests.query.read.default import arguments
from preferences.exceptions import PreferencesError
from preferences.models.Favorite.Favorite import Favorite as FavoriteModel
from preferences.models.Favorite.serializers import FavoriteSerializer


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
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/pointofcontacts.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/requests.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/transitions.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/dispositions.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/favorites.json",
    ]

    @tag("controllers.favorite.fetch_favorites_by_user")
    def test_fetch_favorites_by_user(self) -> None:
        """Success Case: Fetch all `Favorite` records for the given user."""

        favorites = Favorite.fetch_favorites(user=arguments.FETCH_FAVORITE_USER)
        self.assertIsInstance(favorites, QuerySet[FavoriteModel])

        # Serialize `Favorite` instances.
        serialized_favorites = cast(
            list[dict[str, Any]], FavoriteSerializer(favorites, many=True).data
        )

        self.assertListEqual(serialized_favorites, arguments.VALID_FAVORITES)

    @tag("controllers.favorite.fetch_favorites_by_user_dne")
    def test_fetch_favorites_by_user_dne(self) -> None:
        """Fail Case: Fetch all `Favorite` records for
        a `User` that does not exist."""

        with pytest.raises(PreferencesError):
            _ = Favorite.fetch_favorites(user=arguments.FETCH_FAVORITE_USER_DNE)

    @tag("controllers.favorite.fetch_favorited_resources_no_params")
    def test_fetch_favorited_resources_no_params(self) -> None:
        """Success Case: Fetch all favorited resources (resource-level results)."""
        results = Favorite.fetch_favorited_resources(user=arguments.FETCH_FAVORITE_USER)

        # Expect a list of dicts, not a QuerySet of Favorite rows.
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        # Each item should contain a compact resource object and favorite_count.
        for item in results:
            self.assertIsInstance(item, dict)
            self.assertIn("resource", item)
            self.assertIn("favorite_count", item)

            resource = item["resource"]
            self.assertIsInstance(resource, dict)
            self.assertIn("name", resource)
            self.assertIn("url", resource)
            self.assertIn("active", resource)
            self.assertIn("deleted", resource)

            self.assertIsInstance(item["favorite_count"], int)
            self.assertGreaterEqual(item["favorite_count"], 1)

    @tag("controllers.favorite.fetch_favorited_resources_by_user")
    def test_fetch_favorited_resources_by_user(self) -> None:
        """Success Case: Returned resources are actually favorited by the user."""
        user_email = arguments.FETCH_FAVORITE_USER
        results = Favorite.fetch_favorited_resources(user=user_email)

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        # Each returned resource must be favorited by the given user (exists in Favorite rows).
        for item in results:
            resource_name = item["resource"]["name"]
            exists = FavoriteModel.objects.filter(
                resource__name=resource_name, user__email__iexact=user_email
            ).exists()
            self.assertTrue(
                exists, f"Resource {resource_name} should be favorited by {user_email}"
            )

    @tag("controllers.favorite.fetch_favorited_resources_top")
    def test_fetch_favorited_resources_top(self) -> None:
        """Success Case: `top` limits resources ordered by favorite_count descending."""
        top_n = 2
        results = Favorite.fetch_favorited_resources(
            user=arguments.FETCH_FAVORITE_USER, top=top_n
        )

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), top_n)

        # Ensure ordering is descending by favorite_count
        counts = [item["favorite_count"] for item in results]
        self.assertEqual(counts, sorted(counts, reverse=True))

    @tag("controllers.favorite.fetch_favorited_resources_pagination")
    def test_fetch_favorited_resources_pagination(self) -> None:
        """Success Case: Pagination applies to resources (not favorite rows)."""
        # Choose a small page size to exercise pagination
        page = 1
        limit = 2
        results_page_1 = Favorite.fetch_favorited_resources(
            user=arguments.FETCH_FAVORITE_USER, page=page, limit=limit
        )
        self.assertIsInstance(results_page_1, list)
        self.assertLessEqual(len(results_page_1), limit)

        # Fetch page 2 and ensure results are different (if there are enough resources)
        page2 = 2
        results_page_2 = Favorite.fetch_favorited_resources(
            user=arguments.FETCH_FAVORITE_USER, page=page2, limit=limit
        )
        self.assertIsInstance(results_page_2, list)

        # If both pages have results, they should not be identical sets
        if results_page_1 and results_page_2:
            names_page_1 = {r["resource"]["name"] for r in results_page_1}
            names_page_2 = {r["resource"]["name"] for r in results_page_2}
            self.assertNotEqual(names_page_1, names_page_2)

    @tag("controllers.favorite.fetch_favorited_resources_user_dne")
    def test_fetch_favorited_resources_user_dne(self) -> None:
        """Fail Case: Fetch favorited resources for a User that does not exist."""
        with pytest.raises(AnalyticsError):
            _ = Favorite.fetch_favorited_resources(
                user=arguments.FETCH_FAVORITE_USER_DNE
            )
