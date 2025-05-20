"""
`Program Review Tool` `Program` view module. Views handle requests to
fetch and generate reviews for records within the `Program` table.
"""

import logging
from typing import List, Union

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from program_review_tool import controllers, exceptions
from program_review_tool.models.Program.serializers import ProgramSerializer
from program_review_tool.views import serializers

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.settings import SERVER_HOST
from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)

VLE_HOSTNAME_PREFIX: str = "lnvle"


class Program(View):
    """
    Handle user requests to fetch and generate reviews for
    `Program` records within `Program Review Tool`.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.ReviewProgramRequest))
    def post(
        self, request: DjangoHttpRequest, body: dict, _: dict
    ) -> Union[http.JsonResponse, http.StreamingHttpResponse]:
        """Endpoint for POST /program-review-tool/program/review."""
        try:
            LOGGER.info("POST /program-review-tool/program/review.")

            if SERVER_HOST.lower().startswith(VLE_HOSTNAME_PREFIX):
                return http.JsonResponse(
                    "No connection to L3Harris network.",
                    status=status.HTTP_502_BAD_GATEWAY,
                    safe=False,
                )

            review_status, export_path = controllers.Program.review_programs(
                program_ids=body["programs"],
                user=request.user,
                review_name=body["name"],
            )
            if export_path is None:
                return http.JsonResponse(
                    review_status,
                    status=status.HTTP_200_OK,
                    safe=False,
                )
            return http.FileResponse(
                open(export_path, "rb"),
                content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
        except exceptions.ProgramReviewToolError as exc:
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: DjangoHttpRequest, _: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/program-review-tool/program."""

        try:
            req = serializers.FetchProgramRequestQueryParams(data=request.GET)

            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            ids: List[int] = req.validated_data.get("ids")
            page: int = req.validated_data.get("page")
            limit: int = req.validated_data.get("limit")

            request_params = f"?ids={ids}" if ids else ""
            request_params = f"{request_params}&page={page}" if page else request_params
            request_params = (
                f"{request_params}&limit={limit}" if limit else request_params
            )

            LOGGER.info(f"GET /program-review-tool/program{request_params}")

            # Fetch the `Program`(s).
            programs = controllers.Program.fetch_programs(ids, page, limit)

            # Serialize `Program`(s).
            data: List[dict] = ProgramSerializer(programs, many=True).data

            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except exceptions.ProgramReviewToolError as exc:
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
