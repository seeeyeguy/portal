"""
`Usage` represents a use of the `Program Review Tool` by a user.
Each usage committed by a user is stored with our
`Usage` model. `Usage` consists of user(`User`), programs(JSONField),
and created(datetime), duration(DurationField), success(BooleanField),
and error_msg(TextField). A user may have many usages.
"""

# pylint: disable=no-member
from django.contrib.auth import get_user_model
from django.db import models

from portal.models import DateTimeAbstractModel


class Usage(DateTimeAbstractModel):
    """
    `Usage` represents an execution of a portfolio generation.
    `Usage` provides analytical data for `Programs` so that
    `BI Portal` may provide insights and track adoption metrics.
    Actual `Portfolio` IDs do not need to be tracked, only their `Programs`.

    A `Usage` includes:
        * id (int): An auto-generated number managed by the database.
        * user (contrib.auth.models.User): A `BI Portal` user.
        * created (models.DateTimeField): The date & time this `Usage` was created.
        * duration (models.DurationField): How long it took to generate the portfolio.
        * success (models.BooleanField): Was portfolio generation successful.
        * error_msg (models.TextField): Error message if any.
        * programs (models.JSONField): An array of Program PA numbers.
    """

    user = models.ForeignKey(
        get_user_model(), to_field="username", on_delete=models.CASCADE
    )
    duration = models.DurationField(null=True, blank=True)
    success = models.BooleanField(null=True, blank=True)
    error_msg = models.TextField(null=True, blank=True)
    programs = models.JSONField()
    modified = None  # type: ignore[assignment]

    def __str__(self) -> str:
        """String Representation of `Usage`."""
        return (
            f"Usage(id={self.id}, user={self.user.email},"
            f" created={self.created}, duration={self.duration}, success={self.success},"
            f" error_msg={self.error_msg}, programs={self.programs})"
        )

    @property
    def id(self) -> int:
        """Primary Key."""
        return self.id

    class Meta:
        """Meta class for `Usage`."""

        db_table_comment = "Usage represents an execution of a portfolio generation."
        default_related_name = "usages"
        indexes = [
            models.Index(fields=("user",), name="usage_user"),
            models.Index(fields=("id",), name="usage_id"),
        ]
        ordering = ["-created"]
        verbose_name = "usage"
        verbose_name_plural = "usages"


Usage.Meta.db_table_comment = Usage.__doc__  # type: ignore[assignment]
