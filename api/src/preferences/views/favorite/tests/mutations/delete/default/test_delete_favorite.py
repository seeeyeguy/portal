"""Collection of pytests for the Favorite's delete view endpoint."""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from preferences.controllers.Favorite.tests.mutations.delete.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "preferences",
    "favorite",
    "views",
    "preferences.favorite.delete",
    "favorite.delete.default",
    "views.TestDeleteFavorite",
)
class TestDeleteFavorite(MultiDBTestCase):
    """
    Tests for DELETE /v1/preferences/favorites endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.DELETE_FAVORITE_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/Favorite/tests/mutations/delete/default/fixtures/resources.json",
        "preferences/controllers/Favorite/tests/mutations/delete/default/fixtures/pointofcontacts.json",
        "preferences/controllers/Favorite/tests/mutations/delete/default/fixtures/requests.json",
        "preferences/controllers/Favorite/tests/mutations/delete/default/fixtures/transitions.json",
        "preferences/controllers/Favorite/tests/mutations/delete/default/fixtures/dispositions.json",
        "preferences/controllers/Favorite/tests/mutations/delete/default/fixtures/favorites.json",
    ]

    url: str = reverse("preferences.favorite")

    @tag("views.favorite.delete_favorite")
    def test_delete_favorite(self) -> None:
        """Success Case: Delete `Favorite` record with given id."""

        request_url: str = f"{self.url}?id={arguments.DELETE_FAVORITE_FAVORITE_ID}"
        response = self.client.delete(
            request_url, headers={"content-type": "application/json"}
        )
        rows_deleted = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rows_deleted, arguments.DELETE_FAVORITE_DELETED_ROWS)
