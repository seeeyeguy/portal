"""Collection of pytests for the Favorites' fetch view endpoint."""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from preferences.controllers.Favorite.tests.query.read.default import arguments
from portal.models.fixtures import COMMON_FIXTURES
from manager.utils.tests import MultiDBTestCase


@tag(
    "analytics",
    "favorites",
    "views",
    "analytics.favorites.fetch",
    "favorites.fetch.default",
    "views.TestFavoriteView",
)
class TestFavoriteView(MultiDBTestCase):
    """
    Tests for GET /v1/analytics/favorite endpoint.
    """

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/resources.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/favorites.json",
    ]

    url: str = reverse("analytics.favorites")

    def setUp(self) -> None:
        super().setUp()

        # Must match a user email in COMMON_FIXTURES
        self.user = AuthModels.User.objects.get(email=arguments.FETCH_FAVORITE_USER)
        self.client.force_login(user=self.user)

    @tag("views.favorites.create_not_allowed")
    def test_create_favorite_not_allowed(self) -> None:
        """Fail Case: POST to favorites endpoint is not allowed."""
        response = self.client.post(
            self.url,
            {"resource_id": arguments.FETCH_FAVORITE_RESOURCE_ID},
            headers={"content-type": "application/json"},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @tag("views.favorites.fetch_by_user")
    def test_fetch_favorite_by_user(self) -> None:
        """Success Case: Fetch favorites by user email."""
        response = self.client.get(
            self.url,
            {"user": arguments.FETCH_FAVORITE_USER},
            headers={"content-type": "application/json"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        names = [d["resource"]["name"] for d in data]

        self.assertIn(arguments.FETCH_FAVORITE_RESOURCE_NAME, names)

    @tag("views.favorites.fetch_by_resource_id")
    def test_fetch_favorite_by_resource_id(self) -> None:
        """Success Case: Fetch favorites by resource id."""
        response = self.client.get(
            self.url,
            {"resource_id": arguments.FETCH_FAVORITE_RESOURCE_ID},
            headers={"content-type": "application/json"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data[0]["resource"]["name"],
            arguments.FETCH_FAVORITE_RESOURCE_NAME,
        )

    @tag("views.favorites.fetch_with_top")
    def test_fetch_favorites_with_top(self) -> None:
        """Success Case: Fetch favorites with top applied."""
        response = self.client.get(
            self.url,
            {"top": arguments.FETCH_FAVORITE_TOP},
            headers={"content-type": "application/json"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), arguments.FETCH_FAVORITE_TOP)

    @tag("views.favorites.fetch_with_pagination")
    def test_fetch_favorites_with_pagination(self) -> None:
        """Success Case: Fetch favorites with pagination applied."""
        response = self.client.get(
            self.url,
            {
                "limit": arguments.FETCH_FAVORITE_LIMIT,
                "page": arguments.FETCH_FAVORITE_PAGE,
            },
            headers={"content-type": "application/json"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertLessEqual(len(data), arguments.FETCH_FAVORITE_LIMIT)
