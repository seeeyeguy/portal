from django.core.management.base import BaseCommand, CommandError
from jobs.registry import REGISTRY
from django.utils import timezone
from datetime import datetime, timedelta

#TODO: add logging

class Command(BaseCommand):
    help = "Allow execution of background job by name"

    def add_arguments(self, parser):
        parser.add_argument(
            "job_name",
            type = str,
            help = "Name of job to execute"
        )

    def handle(self, *args, **options):
        job_name = options["job_name"]
        
        # Check if job_name is registered
        if job_name not in REGISTRY:
            raise CommandError(f"Job {job_name} not recognized.  Check syntax or jobs.registry.REGISTRY")

        job_function = REGISTRY[job_name]

        #TODO: Add logging
        self.stdout.write(f"Starting job: {job_name}")
        
        started_at_time = timezone.now()
        try:
            job_function()
            finished_at_time = timezone.now()
            duration = finished_at_time - started_at_time 
            # TODO: add write to RunJob
            self.stdout.write(self.style.SUCCESS(f"Job {job_name} completed successfully in {duration.total_seconds()} seconds."))
        except Exception as exc:
            finished_at_time = timezone.now()
            duration = finished_at_time - started_at_time
            self.stdout.write(self.style.ERROR(f"Job {job_name} failed: {exc} in {duration.total_seconds()} seconds"))
            raise CommandError(f"Execution failed for job {job_name}")

