"""
`ProgramMember` represents the association between a `User`,
a `ProgramRole`, and a `Program`. `ProgramMember` provides a
collection of team members for a `Program`, designating their
role as well as the status of that role on the `Program`.
`ProgramMember`s help to execute the `Program` and drive forward
its objectives. Each `User`s role and active status must be unique
on a `Program` (i.e. a `User` cannot have duplicate active roles
on the same `Program`). A `ProgramMember` has a one-to-many relationship
with a `Program`, a one-to-many relationship with a `User`,
and a one-to-many relationship with a `ProgramRole`.
"""

# pylint: disable=no-member
from django.contrib.auth import get_user_model
from django.db import models

from portal.models import DateTimeAbstractModel


class ProgramMember(DateTimeAbstractModel):
    """
    `ProgramMember` represents a team member for a `Program`,
    designating their role as well as the status of that role
    on the `Program`. `ProgramMember`s help to execute the
    `Program` and drive forward its objectives. Current `ProgramMember`
    roles include Program Manager and Program Financial Analyst.

    A `ProgramMember` includes:
        * id (int): An auto-generated number managed by the database.
        * program (models.ForeignKey[program_review_tool.Program]): A `Program` within
            `Program Review Tool`.
        * role (models.ForeignKey[program_review_tool.ProgramRole]): The role of a `ProgramMember`
            on a `Program`.
        * user (models.ForeignKey[django.contrib.auth.User]): A `Program Review Tool` user who is
            a team member of the `Program`.
        * is_active (models.BooleanField): Whether the `User`s role is active on a `Program`.
        * created (models.DateField): The date a `ProgramMember` was added to a `Program`.
        * expiry_date (models.DateField): The date a `ProgramMember` is no longer active
            on the `Program`.
        * modified (models.DateTimeField): The date & time a `ProgramMember` record was
            last modified.
    """

    program = models.ForeignKey("program_review_tool.Program", on_delete=models.CASCADE)
    role = models.ForeignKey(
        "program_review_tool.ProgramRole", to_field="name", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "auth.User", to_field="username", on_delete=models.DO_NOTHING
    )
    is_active = models.BooleanField(null=True, default=None)
    expiry_date = models.DateField(null=True, default=None)

    def __str__(self) -> str:
        """String Representation of a `ProgramMember`."""

        return (
            f"ProgramMember(id={self.id}, user={self.user},"
            f" program={self.program.pa_number}, role={self.role.name})"
        )

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta Class for `ProgramMember`."""

        db_table_comment = ""
        default_related_name = "program_members"
        indexes = [
            models.Index(fields=("program",), name="program_member_program"),
            models.Index(fields=("role",), name="program_member_role"),
            models.Index(fields=("user",), name="program_member_user"),
            models.Index(fields=("id",), name="program_member_id"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["program", "user", "role", "expiry_date"],
                name="program_member_active_team_member",
            )
        ]
        verbose_name = "program_member"
        verbose_name_plural = "program_members"
