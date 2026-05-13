"""
`JobRun` represents a an execution of a job defined in the job registry.
"""


from django.db import models
from portal.models import DateTimeAbstractModel
    
class JobStatus(models.TextChoices):
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    
class JobRun(DateTimeAbstractModel):
    """
    `JobRun` represents an execution of a job defined in the job registry.

    A 'JobRun' includes:
        * job_name (string)
        * user (contrib.auth.models.User)
        * status (enumeration)
        * started_at (models.DateTimeField)
        * finished_at (models.DateTimeField)
        * duration (models.IntegerField)
        * error_msg (models.TextField)
    """

    job_name: models.CharField = models.CharField(max_length=512)

    # JobRun.user may be a local user account running on a server that kicks off the process.
    # If initiated by API call or logged in user, the users username should be used. 
    user: models.CharField = models.CharField(max_length=64, null=True) 
    status: models.CharField = models.CharField(max_length=16, choices=JobStatus) #pyright: ignore[reportArgumentType]
    started_at: models.DateTimeField = models.DateTimeField(null=False)
    finished_at: models.DateTimeField = models.DateTimeField(null=True)
    duration: models.IntegerField = models.IntegerField(default=0, null=True)
    error_msg: models.TextField = models.TextField(null=True)

    def __str__(self) -> str:
        """String Representation of `JobRun`."""

        return (
            f"Job(id={self.id})"
        )

    @property
    def id(self) -> int:
        """Primary Key"""

        return self.pk

    class Meta:
        """Meta class for 'JobRun`"""

        db_table_comment = ""
        default_related_name = "jobruns"
        indexes = [
            models.Index(fields=["job_name"], name="job_name"),
            models.Index(fields=["status"], name="job_status"),
            models.Index(fields=["error_msg"], name="job_error_message"),
        ]
        ordering = ["-finished_at"]
        verbose_name = "jobrun"

JobRun.Meta.db_table_comment = JobRun.__doc__ #type:ignore[assignment]
