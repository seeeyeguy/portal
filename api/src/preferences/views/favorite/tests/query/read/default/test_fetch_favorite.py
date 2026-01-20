"""Collection of pytests for the Favorite's fetch view endpoint."""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from preferences.controllers.Favorite.tests.query.read.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "preferences",
    "favorite",
    "views",
    "preferences.favorite.fetch",
    "favorite.fetch.default",
    "views.TestFetchFavorite",
)
class TestFetchFavorite(MultiDBTestCase):
    """
    Tests for GET /v1/preferences/favorites endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(username=arguments.FETCH_FAVORITE_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/resources.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/pointofcontacts.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/requests.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/transitions.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/dispositions.json",
        "preferences/controllers/Favorite/tests/query/read/default/fixtures/favorites.json",
    ]

    url: str = reverse("preferences.favorite")

    @tag("views.favorite.fetch_favorites_by_user")
    def test_fetch_favorites_by_user(self) -> None:
        """Success Case: Fetch all `Favorite` records for
        the given user."""

        request_url: str = f"{self.url}?user={arguments.FETCH_FAVORITE_USER}"
        response = self.client.get(
            request_url, headers={"content-type": "application/json"}
        )
        favorites = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(favorites, arguments.VALID_FAVORITES)

    @tag("views.favorite.fetch_favorites_by_user_dne")
    def test_fetch_favorites_by_user_dne(self) -> None:
        """Fail Case: Fetch all `Favorite` records for
        a `User` that does not exist."""

        request_url: str = f"{self.url}?user={arguments.FETCH_FAVORITE_USER_DNE}"
        response = self.client.get(
            request_url, headers={"content-type": "application/json"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
