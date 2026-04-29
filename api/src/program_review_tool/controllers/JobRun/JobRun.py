"""
`JobRun` controller module.  Controllers utilize Django ORM to create and fetch 
records within the `JobRun` table. `JobRun` capture information about jobs run.
"""

import logging
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
                status = JobStatus.RUNNING,
            )

            return job_run
        except:
            err_msg = f"Job {job_name} failed"
            
    # @staticmethod
    # def complete_job_run(
    #     job_run_id: int,
    #     status: str,
    #     finished_at: datetime,
    #     error_msg: Optional[str] = None
    # ):
    #     return
    #
    # @staticmethod
    # def fetch_job_run():
    #     return
    #
        
