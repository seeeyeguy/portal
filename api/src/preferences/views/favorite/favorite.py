"""
`BI Portal` `Favorite` view module. Views handle requests to
create, fetch, update, and delete records within the `Favorite`
table. `Favorite` represents a preferred `Resource` for a user.
"""

# Remove pylint disable in implementation story.
# pylint: disable=unused-argument
import logging
from typing import List

from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from preferences import controllers
from preferences.views import serializers

from manager.utils.decorators import with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class Favorite(LoginRequiredMixin, View):
    """
    Handle user requests to create, fetch, update, and delete `Favorite`
    records for `BI Portal`. `Favorite` represents a preferred `Resource`
    for a user.
    """

    @method_decorator(with_serializer(serializers.CreateFavoriteRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/preferences/favorites."""

        LOGGER.info("POST /v1/preferences/favorites.")

        favorite = controllers.Favorite.create_favorite(
            user=body["user"], resource=body["resource"]
        )
        return http.JsonResponse(favorite, status=status.HTTP_201_CREATED)

    @method_decorator(with_serializer(serializers.RankFavoriteRequest, many=True))
    def put(self, request: DjangoHttpRequest, body: List[dict]) -> http.JsonResponse:
        """Endpoint for PUT /v1/preferences/favorites."""

        req = serializers.RankFavoriteQueryParams(data=request.GET)
        if not req.is_valid():
            return http.JsonResponse(
                req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
            )

        user = req.validated_data.get("user")

        LOGGER.info(f"PUT /v1/preferences/favorites?user={user}.")

        instances = controllers.Favorite.rank_favorites(
            user=user, ranked_favorites=body
        )
        return http.JsonResponse(instances, status=status.HTTP_201_CREATED, safe=False)

    @method_decorator(with_serializer(serializers.DeleteFavoriteRequest))
    def delete(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for DELETE /v1/preferences/favorites."""

        LOGGER.info(f"DELETE /v1/preferences/favorites?id={body['id']}.")

        rows_affected = controllers.Favorite.delete_favorite(favorite_id=body["id"])
        return http.JsonResponse(rows_affected, status=status.HTTP_200_OK, safe=False)

    @method_decorator(with_serializer(serializers.FetchFavoriteRequest))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/preferences/favorites."""

        LOGGER.info(f"GET /v1/preferences/favorites?user={body['user']}.")

        favorites = controllers.Favorite.fetch_favorites(user=body["user"])
        return http.JsonResponse(favorites, status=status.HTTP_200_OK, safe=False)
