"""
`BI Portal` `Resource` view module. Views handle requests to
create, fetch, search, update, and delete records within the
`Resource` table. `Resource` represents a link to an internal
tool within L3Harris technologies. `Resource` is the primary
content served by `BI Portal`.
"""

# Remove pylint disable in implementation story.
# pylint: disable=unused-argument
import logging
from typing import List, Union

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from directory.controllers.Resource.Resource import (
    CreateResourceParams,
    Resource as ResourceController,
    ResourceSearch as ResourceSearchController,
    SearchParams,
    UpdateResourceParams,
)
from directory.controllers.Resource.search.utils import FUNCTREE_STRUCTURE
from directory.exceptions import DirectoryError
from directory.models.Resource.serializers import ResourceSerializer

from directory.views import serializers

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class Resource(APIView):
    """
    Handle user requests to create, fetch, update, and delete `Resource`
    records for `BI Portal`. `Resource` represents a link to an internal
    tool within L3Harris technologies.
    """

    parser_classes = (FormParser, MultiPartParser)

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.CreateResourceRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/directory/resources."""

        try:
            LOGGER.info(f"POST /v1/directory/resources.")

            create_params: CreateResourceParams = CreateResourceParams(
                uid=body["uid"],
                name=body["name"],
                description=body["description"],
                previous_revision=body["previous_revision"],
                url=body["url"],
                thumbnail=body["thumbnail"],
                employee_levels=body["employee_levels"],
                subfunctions=body["subfunctions"],
                tags=body["tags"],
                type=body["type"],
                download=body["download"],
                user=request.user,
            )

            resource = ResourceController.create_resource(params=create_params)

            data: dict = ResourceSerializer(resource).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except DirectoryError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.UpdateResourceRequest))
    def put(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for PUT /v1/directory/resources."""

        try:
            req = serializers.UpdateResourceRequestQueryParams(data=request.GET)
            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            resource_id = req.validated_data.get("id")

            LOGGER.info(f"PUT /v1/directory/resources?id={resource_id}.")

            update_params: UpdateResourceParams = UpdateResourceParams(
                resource_id=resource_id,
                name=body["name"],
                description=body["description"],
                url=body["url"],
                thumbnail=body["thumbnail"],
                employee_levels=body["employee_levels"],
                subfunctions=body["subfunctions"],
                tags=body["tags"],
                type=body["type"],
                download=body["download"],
                user=request.user,
            )

            resource, _ = ResourceController.update_resource(params=update_params)

            # Serialize `Resource` instance.
            data: dict = ResourceSerializer(resource).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except DirectoryError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(with_serializer(serializers.FetchResourceRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/directory/resources."""

        try:
            request_params = f"?id={body['id']}" if body["id"] else ""
            request_params = f"?page={body['page']}" if body["page"] else request_params
            request_params = (
                f"{request_params}{'&' if body['page'] else '?'}limit={body['limit']}"
                if body["limit"]
                else request_params
            )

            LOGGER.info(f"GET /v1/directory/resources{request_params}.")

            resources = ResourceController.fetch_resources(
                resource_id=body["id"], page=body["page"], limit=body["limit"]
            )

            many: bool = body["id"] is None

            # Serialize `Resource` instance.
            data: Union[dict | List[dict]] = ResourceSerializer(
                resources, many=many
            ).data

            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except DirectoryError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)


class ResourceSearch(View):
    """
    Handle user requests to search for `Resource` records in `BI Portal`.
    `Resource` represents a link to an internal tool within L3Harris
    technologies.
    """

    @method_decorator(
        with_serializer(serializer_class=serializers.ResourceSearchRequest)
    )
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/directory/resources/search."""

        try:
            req = serializers.ResourceSearchQueryParams(data=request.GET)
            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            page = req.validated_data.get("page")
            limit = req.validated_data.get("limit")

            request_params = f"?page={page}" if page else ""
            request_params = (
                f"{request_params}{'&' if page else '?'}limit={limit}"
                if limit
                else request_params
            )

            LOGGER.info(f"POST /v1/directory/resources/search{request_params}.")

            # Get the structure for the search from the body
            structure = body["structure"]
            # Ensure serialize is set to True if search structure
            # is `functree`.
            serialize = structure == FUNCTREE_STRUCTURE

            # Construct search parameters for controller.
            search_params: SearchParams = SearchParams(
                name=body["name"],
                description=body["description"],
                functions=body["functions"],
                subfunctions=body["subfunctions"],
                employee_levels=body["employee_levels"],
                tags=body["tags"],
                download=body["download"],
                structure=structure,
                serialize=serialize,
                limit=limit,
                page=page,
            )
            # Invoke search controller function.
            search_results = ResourceSearchController.search(search_params)
            # If the structure of the search is `functree` then assign
            # `search_results` directly to data else apply the `Resource`
            # serializer to the results and assign its data.
            data = (
                search_results
                if structure == FUNCTREE_STRUCTURE
                else ResourceSerializer(search_results, many=True).data
            )
            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)

        except DirectoryError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
