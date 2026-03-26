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
from manager.settings import ApplicationBuild, BUILD, SERVER_HOST
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

            if (
                SERVER_HOST.lower().startswith(VLE_HOSTNAME_PREFIX)
                and BUILD != ApplicationBuild.TEST
            ):
                return http.JsonResponse(
                    "No connection to L3Harris network.",
                    status=status.HTTP_502_BAD_GATEWAY,
                    safe=False,
                )

            review_status, export_path = controllers.Program.review_programs(  # type: ignore[attr-defined]
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
            filename: str = export_path.split("/")[-1]
            response = http.FileResponse(
                open(export_path, "rb"),
                content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                status=status.HTTP_201_CREATED,
            )
            response["Content-Disposition"] = f"attachment;filename={filename}"
            return response
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
            pa_numbers: List[str] = req.validated_data.get("pa_numbers")
            program_member: str = req.validated_data.get("program_member")
            tiers: List[int] = req.validated_data.get("tiers")
            segments: List[int] = req.validated_data.get("segments")
            page: int = req.validated_data.get("page")
            limit: int = req.validated_data.get("limit")
            active_only: bool = not (
                request.GET.get("active_only", "true").lower() == "false"
            )

            request_params = f"?ids={ids}" if ids else ""
            request_params = (
                f"{request_params}{'&' if request_params else '?'}pa_numbers={pa_numbers}"
                if pa_numbers
                else request_params
            )
            request_params = (
                f"{request_params}{'&' if request_params else '?'}program_member={program_member}"
                if program_member
                else request_params
            )
            request_params = (
                f"{request_params}{'&' if request_params else '?'}tiers={tiers}"
                if tiers
                else request_params
            )
            request_params = (
                f"{request_params}{'&' if request_params else '?'}segments={segments}"
                if segments
                else request_params
            )
            request_params = (
                f"{request_params}{'&' if request_params else '?'}active_only={active_only}"
                if active_only
                else request_params
            )
            request_params = (
                f"{request_params}{'&' if request_params else '?'}page={page}"
                if page
                else request_params
            )
            request_params = (
                f"{request_params}{'&' if request_params else '?'}limit={limit}"
                if limit
                else request_params
            )

            LOGGER.info(f"GET /program-review-tool/program{request_params}")

            # Fetch the `Program`(s).
            programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
                program_ids=ids,
                pa_numbers=pa_numbers,
                tiers=tiers,
                segments=segments,
                active_only=active_only,
                program_member=program_member,
                page=page,
                limit=limit,
            )

            # Serialize `Program`(s).
            data: List[dict] = ProgramSerializer(programs, many=True).data

            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except exceptions.ProgramReviewToolError as exc:
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
