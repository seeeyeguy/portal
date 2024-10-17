"""
`BI Portal` `Tag` view module. Views handle requests to
create, fetch, update, and delete records within the `Tag`
table. `Tag` helps to categorize resources through keywords
represented by labels.
"""

import logging
from typing import List, Union

from django import http
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from directory import controllers, exceptions, models
from directory.models.Tag.serializers import TagSerializer
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

        try:
            request_params = f"?id={body['id']}" if body["id"] else ""
            request_params = f"?page={body['page']}" if body["page"] else request_params
            request_params = (
                f"{request_params}{'&' if body['page'] else '?'}limit={body['limit']}"
                if body["limit"]
                else request_params
            )
            LOGGER.info(f"GET /v1/directory/tags{request_params}")

            # Fetch the `Tag`(s).
            tags = controllers.Tag.fetch_tags(
                tag_id=body["id"], page=body["page"], limit=body["limit"]
            )

            # Determine the value for `many` parameter on the serializer.
            many: bool = body["id"] is None

            # Serialize `Tag`(s).
            data: Union[dict | List[dict]] = TagSerializer(tags, many=many).data
            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except exceptions.DirectoryError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)


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

        # Search for `Tag`s that start with the given label.
        search_tag_results: QuerySet[
            models.Tag, models.Tag
        ] = controllers.Tag.search_tags(label=body["label"])
        data: List[dict] = TagSerializer(search_tag_results, many=True).data
        return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
