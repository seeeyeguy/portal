"""
`BI Portal` `Request` view module. Views handle requests to
create, fetch, and update records within the `Request` table.
`Request` represent a request by a `User` to create, update,
or delete a `Resource` record within `BI Portal`. A `Resource`
record must be related to a `Request` that has been processed
through the `BI Portal` request workflow with the needed
approvals before any change can be made in `BI Portal`'s
published `Resource` record dataset.
"""

import logging
from typing import List, Union

from django import http
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from request.controllers.Request.Request import (
    CreateRequestParams,
    DeleteRequestParams,
    Request as RequestController,
    UpdateRequestParams,
)
from request.exceptions import RequestError
from request.models.Request.serializers import RequestSerializer
from request.views import serializers

from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


@method_decorator(never_cache, name="dispatch")
class Request(APIView):
    """
    Handle user requests to create, fetch, or update `Request`
    records for `BI Portal`. `Request` represent a request
    by a `User` to create, update, or delete a `Resource`
    record within `BI Portal`.
    """

    parser_classes = (FormParser, MultiPartParser)

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.CreateRequestRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/request/request."""

        try:
            LOGGER.info("POST /v1/request/request.")

            create_params: CreateRequestParams = CreateRequestParams(  # type: ignore[typeddict-item]
                uid=body["uid"],
                name=body["name"],
                description=body["description"],
                previous_revision=body["previous_revision"],
                url=body["url"],
                thumbnail=body["thumbnail"],
                employee_levels=body["employee_levels"],
                subfunctions=body["subfunctions"],
                tags=body["tags"],
                point_of_contacts=body["point_of_contacts"],
                type=body["type"],
                download=body["download"],
                user=request.user,
                originator=request.user,
                stage=body["stage"],
            )

            # Create a `Request` record.
            request_record = RequestController.create_request(create_params)

            # Serialize `Request` instance.
            data: dict = RequestSerializer(request_record).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except RequestError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.UpdateRequestRequest))
    def put(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for PUT /v1/request/request."""

        try:
            req = serializers.UpdateRequestRequestQueryParams(data=request.GET)
            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            request_id = req.validated_data.get("id")

            log_msg = f"PUT /v1/request/request?id={request_id}."

            LOGGER.info(log_msg)

            update_params: UpdateRequestParams = UpdateRequestParams(
                request_id=request_id,
                name=body["name"],
                description=body["description"],
                url=body["url"],
                thumbnail=body["thumbnail"],
                employee_levels=body["employee_levels"],
                subfunctions=body["subfunctions"],
                tags=body["tags"],
                point_of_contacts=body["point_of_contacts"],
                type=body["type"],
                download=body["download"],
                user=request.user,
                stage=body["stage"],
            )

            # Update a `Request` record.
            request_record, _ = RequestController.update_request(update_params)

            # Serialize `Request` instance.
            data: dict = RequestSerializer(request_record).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except RequestError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.DeleteRequestRequestQueryParams))
    def delete(self, request: DjangoHttpRequest, _body: dict) -> http.JsonResponse:
        """Endpoint for DELETE /v1/request/request."""

        try:
            req = serializers.DeleteRequestRequestQueryParams(data=request.GET)
            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            resource_id = req.validated_data.get("id")

            log_msg = f"DELETE /v1/request/request?id={resource_id}."

            LOGGER.info(log_msg)

            delete_params: DeleteRequestParams = DeleteRequestParams(
                resource_id=resource_id,
                originator=request.user,
            )

            # Create a `Request` to delete a `Resource` record.
            _ = RequestController.delete_request(delete_params)

            return http.JsonResponse(1, status=status.HTTP_202_ACCEPTED, safe=False)
        except RequestError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(with_serializer(serializers.FetchRequestRequest))
    def get(self, _: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/request/request."""

        try:
            log_msg = (
                f"GET /v1/request/request?id={body['id']}",
                f"&originator={body['originator']}&stage={body['stage']}",
                f"&status={body['status']}&page={body['page']}&limit={body['limit']}",
                f"&include_archived={body['include_archived']}",
            )
            LOGGER.info(log_msg)

            # Fetch `Request` records that satisfy given params.
            request_records = RequestController.fetch_requests(
                request_id=body["id"],
                originator=body["originator"],
                stage=body["stage"],
                status=body["status"],
                page=body["page"],
                limit=body["limit"],
                include_archived=body["include_archived"],
            )

            many: bool = body["id"] is None

            # Serialize `Request` instance.
            data: Union[dict | List[dict]] = RequestSerializer(
                request_records, many=many
            ).data

            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except RequestError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
