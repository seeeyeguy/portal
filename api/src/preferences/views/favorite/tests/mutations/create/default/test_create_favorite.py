"""Collection of pytests for the Favorite's create view endpoint."""

from typing import List

from django.contrib.auth.models import User
from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from portal.models.fixtures import COMMON_FIXTURES
from preferences.controllers.Favorite.tests.mutations.create.default import arguments


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

    def setUp(self) -> None:

        super().setUp()
        user = User.objects.get(email=arguments.CREATE_FAVORITE_USER)
        self.client.force_login(user=user)

    # pylint: disable=line-too-long
    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/Favorite/tests/mutations/create/default/fixtures/resources.json",
        "preferences/controllers/Favorite/tests/mutations/create/default/fixtures/requests.json",
        "preferences/controllers/Favorite/tests/mutations/create/default/fixtures/transitions.json",
        "preferences/controllers/Favorite/tests/mutations/create/default/fixtures/dispositions.json",
        "preferences/controllers/Favorite/tests/mutations/create/default/fixtures/favorites.json",
    ]

    url: str = reverse("preferences.favorite")

    @tag("views.favorite.create_favorite")
    def test_create_favorite(self) -> None:
        """Success Case: Create a `Favorite` record."""

        body: dict = {"resource": arguments.CREATE_FAVORITE_RESOURCE_ID}

        # Make request to create `Favorite`.
        response = self.client.post(self.url, body, content_type="application/json")

        favorite = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(favorite, dict)

        # Remove dynamic primary key and datetime fields before comparison.
        del favorite["id"]
        del favorite["created"]

        self.assertEqual(favorite, arguments.CREATE_FAVORITE_EXPECTED_VALUES)

    @tag("views.favorite.create_favorite_resource_dne")
    def test_create_favorite_resource_dne(self) -> None:
        """Fail Case: Create a `Favorite` record with a given resource id
        where that `Resource` does not exist."""

        body: dict = {"resource": arguments.CREATE_FAVORITE_RESOURCE_DNE}

        # Make request to create `Favorite`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.favorite.create_favorite_existing_favorite")
    def test_create_favorite_existing_favorite(self) -> None:
        """Fail Case: Create a `Favorite` record with a `Favorite` record that
        already exists for the given `User` and `Resource`."""

        body: dict = {
            "resource": arguments.CREATE_FAVORITE_EXISTING_FAVORITE_RESOURCE_ID
        }

        # Make request to create `Favorite`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 400.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.favorite.create_favorite_inactive_resource")
    def test_create_favorite_inactive_resource(self) -> None:
        """Fail Case: Create a `Favorite` record with a given resource id
        where that `Resource` is inactive."""

        body: dict = {"resource": arguments.CREATE_FAVORITE_INACTIVE_RESOURCE_ID}

        # Make request to create `Favorite`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
