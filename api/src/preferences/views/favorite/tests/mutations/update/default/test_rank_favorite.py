"""Collection of pytests for the Favorite's rank view endpoint."""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from portal.models.fixtures import COMMON_FIXTURES
from preferences.controllers.Favorite.tests.mutations.update.default import arguments


@tag(
    "preferences",
    "favorite",
    "views",
    "preferences.favorite.rank",
    "favorite.rank.default",
    "views.TestRankFavorite",
)
class TestRankFavorite(TestCase):
    """
    Tests for PUT /v1/preferences/favorites endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.RANK_FAVORITE_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/Favorite/tests/mutations/update/default/fixtures/resources.json",
        "preferences/controllers/Favorite/tests/mutations/update/default/fixtures/requests.json",
        "preferences/controllers/Favorite/tests/mutations/update/default/fixtures/transitions.json",
        "preferences/controllers/Favorite/tests/mutations/update/default/fixtures/dispositions.json",
        "preferences/controllers/Favorite/tests/mutations/update/default/fixtures/favorites.json",
    ]

    url: str = reverse("preferences.favorite")

    @tag("views.favorite.rank_favorites")
    def test_rank_favorites(self) -> None:
        """Success Case: Rank a user's favorites."""

        request_url: str = f"{self.url}?user={arguments.RANK_FAVORITE_USER_EMAIL}"
        response = self.client.put(
            request_url,
            arguments.RANK_FAVORITE_RANKED_FAVORITES_PARAM,
            content_type="application/json",
        )
        favorites = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertListEqual(favorites, arguments.VALID_RANKED_FAVORITES)

    @tag("views.favorite.rank_favorites_user_dne")
    def test_rank_favorites_user_dne(self) -> None:
        """Fail Case: Rank a user's favorites for a `User`
        that does not exist."""

        request_url: str = f"{self.url}?user={arguments.RANK_FAVORITE_USER_EMAIL_DNE}"
        response = self.client.put(
            request_url,
            arguments.RANK_FAVORITE_RANKED_FAVORITES_PARAM,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.favorite.rank_favorites_favorite_dne")
    def test_rank_favorites_favorite_dne(self) -> None:
        """Fail Case: Rank a user's favorites where a `Favorite`
        does not exist for the user."""

        request_url: str = f"{self.url}?user={arguments.RANK_FAVORITE_USER_EMAIL}"
        response = self.client.put(
            request_url,
            arguments.RANK_FAVORITE_RANKED_FAVORITES_PARAM_FAVORITE_DNE,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.favorite.rank_favorites_mismatch_ranks")
    def test_rank_favorites_mismatch_ranks(self) -> None:
        """Fail Case: Rank a user's favorites where there is
        a mismatch between the existing ranks and the ones
        being supplied in the update."""

        request_url: str = f"{self.url}?user={arguments.RANK_FAVORITE_USER_EMAIL}"
        response = self.client.put(
            request_url,
            arguments.RANK_FAVORITE_RANKED_FAVORITES_PARAM_MISMATCH_RANKS,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.favorite.rank_favorites_duplicate_ranks")
    def test_rank_favorites_duplicate_ranks(self) -> None:
        """Fail Case: Rank a user's favorites where several favorites
        have a duplicate rank."""

        request_url: str = f"{self.url}?user={arguments.RANK_FAVORITE_USER_EMAIL}"
        response = self.client.put(
            request_url,
            arguments.RANK_FAVORITE_RANKED_FAVORITES_PARAM_DUPLICATE_RANK,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
