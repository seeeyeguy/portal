"""
`BI Portal` `Tag` view module. Views handle requests to
create, fetch, update, and delete records within the `Tag`
table. `Tag` helps to categorize resources through keywords
represented by labels.
"""

import logging

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from directory.views import serializers

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import with_serializer

LOGGER = logging.getLogger(__name__)


class Tag(View):
    """
    Handle user requests to create, fetch, update, and delete `Tag`
    records for `BI Portal`. `Tag` classifies a resource with
    keywords to better help users search and filter resource records.
    """

    @method_decorator(with_serializer(serializers.FetchTagRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/directory/tags."""

        request_params = f"?id={body['id']}" if body["id"] else ""
        LOGGER.info(f"GET /v1/directory/tags{request_params}")
        return http.JsonResponse([], status=status.HTTP_200_OK, safe=False)


class TagSearch(View):
    """
    Handle user requests to search for `Tag` records within `BI Portal`.
    This request returns a list of `Tag` records based on the provided
    label using a `startswith` style search. These records are used to provide
    insights to the user about preexisting tags.
    """

    @method_decorator(with_serializer(serializers.TagSearchRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/directory/tags/search."""

        LOGGER.info(f"GET /v1/directory/tags/search?label={body['label']}")
        return http.JsonResponse([], status=status.HTTP_200_OK, safe=False)
