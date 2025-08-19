"""
`ProgramRole` represents the specific role that is assigned to
a `ProgramMember` on a `Program`. A `ProgramRole` consists of either
a Program Manager (PGM) or a Program Financial Analyst (PFA). `ProgramRole`
helps assign a specific role to a 'ProgramMember' record. These `ProgramRole`s
will help identify the specific `ProgramRole` a `ProgramMember` may have on a specific
`Program`. `ProgramRole` shares a one-to-many relationship with `ProgramMember`.
"""

from django.db import models

from portal.models import BasicInformationAbstractModel, DateTimeAbstractModel


class ProgramRole(BasicInformationAbstractModel, DateTimeAbstractModel):
    """
    `ProgramRole` represents a collection of specific roles that a
    `ProgramMember` can have. These records provide a curated set of
    roles on a `Program` and help to increase the efficiency and ease of
    use of our queries.

    A `ProgramRole` includes:
        * id (int): An auto-generated number managed by the database.
        * name (models.CharField): The name of the `ProgramRole`.
        * description (models.CharField): The description of a role's
            activities on a `Program`.
        * created (models.DateTimeField): The date & time this `ProgramRole` was created.
        * modified (models.DateTimeField): The date & time this `ProgramRole` was last modified.
    """

    class ProgramRoles:
        """Valid team member roles for a `Program`."""

        PROGRAM_MANAGER = 1
        PROGRAM_FINANCIAL_ANALYST = 2

    def __str__(self) -> str:
        """String Representation of a `ProgramRole`."""

        return f"ProgramRole(id={self.id}, name={self.name})"

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta Class for `ProgramRole`."""

        db_table_comment = ""
        default_related_name = "program_role"
        indexes = [
            models.Index(fields=("name",), name="program_role_name"),
            models.Index(fields=("id",), name="program_role_id"),
        ]
        verbose_name = "program_role"
        verbose_name_plural = "program_roles"
