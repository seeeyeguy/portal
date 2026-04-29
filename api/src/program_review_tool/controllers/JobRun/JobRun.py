"""
`JobRun` controller module.  Controllers utilize Django ORM to create and fetch 
records within the `JobRun` table. `JobRun` capture information about jobs run.
"""

import logging
from typing import Optional
from django.contrib.auth import models as AuthModels
from datetime import datetime, timezone
from program_review_tool.models.JobRun.JobRun import JobStatus
from program_review_tool import exceptions, models

LOGGER = logging.getLogger(__name__)

class JobRun:

    @staticmethod
    def create_job_run(job_name: str, status: str, user: AuthModels.User, started_at: datetime) -> models.JobRun:
        """
        Create a `JobRun` record in the database given a ...
        TODO: add more description

        Accepts:
            * user
            * status
            * started_at
        """
        try:
            LOGGER.info("Creating JobRun for User: {user} for job: {job}")

            # Fetch the users record
            user_record = AuthModels.User.objects.get(
                username__iexact=user
            )
            
            # Create the `JobRun` record
            job_run: models.JobRun = models.JobRun.objects.create(
                job_name = job_name,
                user = user_record,
                status = JobStatus.RUNNING,
                started_at = started_at,
            )

            return job_run
            
        except AuthModels.User.DoesNotExist as exc:
            err_msg = f"User (username={user}) does not exist."
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

    # @staticmethod
    # def fetch_job_run():
    #     return
    #
        
