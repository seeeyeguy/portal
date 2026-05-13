"""
`JobRun` controller module.  Controllers utilize Django ORM to create and fetch 
records within the `JobRun` table. `JobRun` capture information about jobs run.
"""

import logging
from typing import Optional
from django.contrib.auth import models as AuthModels
from datetime import datetime 

from django.db.models import QuerySet
from analytics import exceptions as analytics_exceptions
from program_review_tool.models.JobRun.JobRun import JobStatus
from program_review_tool import exceptions, models

LOGGER = logging.getLogger(__name__)

class JobRun:

    @staticmethod
    def create_job_run(job_name: str, username: str, started_at: datetime) -> models.JobRun:
        """
        Create a `JobRun` record in the database given a ...
        TODO: add more description

        Accepts:
            * user
            * status
            * started_at
        """
        try:
            LOGGER.info(f"Creating JobRun for User: {username} for job: {job_name}")

            # Fetch the users record
            user_record = AuthModels.User.objects.get(
                username__iexact=username
            )
            
            # Create the `JobRun` record
            job_run: models.JobRun = models.JobRun.objects.create(
                job_name = job_name,
                user = user_record.username,
                status = JobStatus.RUNNING,
                started_at = started_at,
            )

            return job_run
            
        except AuthModels.User.DoesNotExist as exc:
            err_msg = f"User (username={username}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404) from exc

    @staticmethod
    def complete_job_run(
        job_run_id: int,
        status: str,
        finished_at: Optional[datetime] = None,
        error_msg: Optional[str] = None
    ) -> models.JobRun:

        # Fetch job_run
        job_run: models.JobRun = models.JobRun.objects.get(
            id = job_run_id
        )
        
        duration = None
        if finished_at:
            duration = job_run.finished_at - job_run.started_at

        # Update job_run fields
        job_run.duration = duration
        job_run.finished_at = finished_at
        job_run.status = status
        job_run.error_msg = error_msg

        job_run.save()

        return job_run

    @staticmethod
    def fetch_job_run(
        page: Optional[int] = None,
        limit: Optional[int] = None,
        status: Optional[str] = None
    ):
        try:
            LOGGER.info(f"Fetching JobRun - page:{page}, limit: {limit}")
            
            if page is not None and page < 1:
                raise analytics_exceptions.AnalyticsError(
                    "Page must be a positive integer.", 400
                )

            if limit is not None and limit < 1:
                raise analytics_exceptions.AnalyticsError(
                    "Limit must be a postive interger.", 400
                )

            if status is not None and status not in JobStatus:
                raise analytics_exceptions.AnalyticsError(
                    "Status not recognzied.", 400
                )

           # Construct the base queryset for all JobRun records
            job_runs: QuerySet[models.JobRun] = models.JobRun.objects.all().order_by("-created")

            # Filter by status
            if status:
                job_runs = job_runs.filter(status=status)

            # Paginate
            if page is not None and limit:
                start = (page - 1) * limit
                end = start + limit
                return job_runs[start:end]

            return job_runs
        except Exception as exc:
            err_msg = f"Unexpected error fetching JobRun records: {exc}"
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 500) from exc
            
        return
        
