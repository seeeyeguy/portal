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
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from preferences import controllers, exceptions
from preferences.models.Favorite.serializers import FavoriteSerializer
from preferences.views import serializers
from preferences.utils.constants.response import CACHE_CONTROL_NO_CACHE

from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class Favorite(View):
    """
    Handle user requests to create, fetch, update, and delete `Favorite`
    records for `BI Portal`. `Favorite` represents a preferred `Resource`
    for a user.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.CreateFavoriteRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/preferences/favorites."""

        try:
            LOGGER.info("POST /v1/preferences/favorites.")

            # Call controller to create `Favorite`.
            favorite = controllers.Favorite.create_favorite(
                user=request.user.email, resource=body["resource"]
            )

            # Serialize `Favorite`.
            data: dict = FavoriteSerializer(favorite).data
            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except exceptions.PreferencesError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.RankFavoriteRequest, many=True))
    def put(self, request: DjangoHttpRequest, body: List[dict]) -> http.JsonResponse:
        """Endpoint for PUT /v1/preferences/favorites."""

        try:
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
            # Serialize `Favorite` instances.
            data: dict = FavoriteSerializer(instances, many=True).data
            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except exceptions.PreferencesError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(data=exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.DeleteFavoriteRequest))
    def delete(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for DELETE /v1/preferences/favorites."""

        try:
            LOGGER.info(f"DELETE /v1/preferences/favorites?id={body['id']}.")

            rows_affected = controllers.Favorite.delete_favorite(favorite_id=body["id"])
            return http.JsonResponse(
                rows_affected, status=status.HTTP_200_OK, safe=False
            )
        except exceptions.PreferencesError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(data=exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.FetchFavoriteRequest))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/preferences/favorites."""

        try:
            LOGGER.info(f"GET /v1/preferences/favorites?user={body['user']}.")

            favorites = controllers.Favorite.fetch_favorites(user=body["user"])

            # Serialize `Favorite` instances.
            data: dict = FavoriteSerializer(favorites, many=True).data
            return http.JsonResponse(
                data,
                status=status.HTTP_200_OK,
                headers={**CACHE_CONTROL_NO_CACHE},
                safe=False,
            )
        except exceptions.PreferencesError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(data=exc.message, status=exc.status, safe=False)
