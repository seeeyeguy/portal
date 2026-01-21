import logging
from typing import Any

from django import http
from django.http import HttpRequest as DjangoHttpRequest
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from analytics import exceptions
from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import with_serializer
from analytics.views.serializers.favorite import FetchFavoritesRequest
from preferences.controllers.Favorite import Favorite as FavoriteController

LOGGER = logging.getLogger(__name__)


class FavoriteView(View):
    """
    Handle user requests to create, fetch, update, and delete `Favorite`
    records for `BI Portal`.
    """

    @method_decorator(with_serializer(serializer_class=FetchFavoritesRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(
        self, request: DjangoHttpRequest, params: dict, *args: Any, **kwargs: Any
    ) -> http.JsonResponse:
        """Endpoint for GET /v1/analytics/favorite."""
        # `params` is the validated serializer data injected by the decorator
        try:
            results = FavoriteController.fetch_favorited_resources(
                user=params.get("user"),
                top=params.get("top"),
                page=params.get("page"),
                limit=params.get("limit"),
            )
            return http.JsonResponse(results, status=status.HTTP_200_OK, safe=False)

        except exceptions.AnalyticsError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(
                {"detail": exc.message}, status=exc.status, safe=False
            )
