"""
`Program Review Tool` `Program` view module. Views handle requests to
fetch and generate reviews for records within the `Program` table.
"""

import logging
from typing import List

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from program_review_tool import controllers, exceptions
from program_review_tool.models.Program.serializers import ProgramSerializer
from program_review_tool.views import serializers

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class Program(View):
    """
    Handle user requests to fetch and generate reviews for
    `Program` records within `Program Review Tool`.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.ReviewProgramRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /program-review-tool/program/review."""

        try:
            LOGGER.info("POST /program-review-tool/program/review.")

            review_status = controllers.Program.review_programs(
                program_ids=body["program_ids"],
                user=request.user,
                review_name=body["review_name"],
            )

            return http.JsonResponse(
                review_status, status=status.HTTP_201_CREATED, safe=False
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

            LOGGER.info(f"GET /program-review-tool/program?ids={ids}")

            # Fetch the `Program`(s).
            programs = controllers.Program.fetch_programs(ids)

            # Serialize `Program`(s).
            data: List[dict] = ProgramSerializer(programs, many=True).data

            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except exceptions.ProgramReviewToolError as exc:
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
