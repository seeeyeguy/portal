"""
`JobRun` view module.
"""

import logging
from django import http
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.utils import timezone
from program_review_tool import controllers
from django.views import View
from rest_framework import status

from analytics import exceptions
from program_review_tool.views import serializers
from program_review_tool.controllers import JobRun as JobRunController
from program_review_tool.models.JobRun.serializers import JobRunSerializer
from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)

@method_decorator(never_cache, name="dispatch")
class JobRun(View):
    """
    Handle user requests to create and fetch
    `JobRun`s.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializer_class=serializers.CreateJobRunRequest))
    def post(self, request: DjangoHttpRequest, body:dict) -> http.JsonResponse:
        """Endpoint for POST /program-review-tool/jobrun"""

        LOGGER.info("POST /program-review-tool/jobrun")
        LOGGER.info(f"Payload : {body}")

        try:
            LOGGER.info("POST /program-review-tool/jobrun")

            username: str = request.user.username 

            # Create job run
            job_run = controllers.JobRun.create_job_run(
                job_name = body["job_name"],
                username = username,
                started_at=timezone.now()
            )

            # Serialize job run
            data: dict = dict(JobRunSerializer(job_run).data)
            return http.JsonResponse(data, status=status.HTTP_201_CREATED)
        except exceptions.AnalyticsError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    def get(self, request: DjangoHttpRequest) -> http.JsonResponse:
        """Endpoint for GET /program-review-tool/job-run"""
        try:
            page = request.GET.get("page")
            limit = request.GET.get("limit")
            status_filter = request.GET.get("status")

            page = int(page) if page is not None else None
            limit = int(limit) if limit is not None else None

            LOGGER.info(f"GET /program-review-tool/job-run?page={page}&limit={limit}&status={status_filter}")

            jobs = JobRunController.fetch_job_run(
                page=page,
                limit=limit,
                status=status_filter,
            )
            data = JobRunSerializer(jobs, many=True).data
            return http.JsonResponse(list(data), status=status.HTTP_200_OK, safe=False)
        except exceptions.AnalyticsError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

class JobRunRegistry(View):
    @method_decorator(login_required())
    def get(self, request: DjangoHttpRequest) -> http.JsonResponse:
            """Endpoing for Get /program-review-tool/jobs"""

            from jobs import REGISTRY
            
            try:
                data = [{"job_name": name, "function_name": func} for name, func in REGISTRY]

                return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
            except exceptions.AnalyticsError as exc:
                return http.JsonResponse(exc, status=exc.status, safe=False)



                
    

