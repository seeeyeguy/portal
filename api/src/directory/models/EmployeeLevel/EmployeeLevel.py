"""
`EmployeeLevel` represents a strictly defined set of
filters associated with resources consisting of a
name(str), description(str), and level (int). As of
08/06/2024, `EmployeeLevel` is restricted to the values of
`EMPLOYEE`, `MANAGER`, and `EXECUTIVE`. `EmployeeLevel` can
be associated with many `Resource`s and a `Resource` may be
related to many `EmployeeLevel`s. This many-to-many relationship
conveys a method of categorizing, grouping, and filtering
resources by their employee level. Of note, name is not the
value of an `EmployeeLevel` but a human-readable representation
of level (`EmployeeLevel`'s true value).
"""

from django.db import models

from portal.models import BasicInformationAbstractModel, DateTimeAbstractModel


class EmployeeLevel(BasicInformationAbstractModel, DateTimeAbstractModel):
    """
    `EmployeeLevel` represents a hierarchical level of leadership within
    the organization and a level of concern for a resource. Employee Levels
    help to classify a resource, and provide metadata. Employee Levels are
    a strictly defined set created by a superuser.

    An `EmployeeLevel` includes:
        * id (int): An auto-generated number managed by the database.
        * name (models.CharField): The name of the `EmployeeLevel`.
        * description (models.CharField): A short/detailed description of what
            this `EmployeeLevel` is.
        * level (models.PositiveIntegerField): An immutable numerical representation
            of an `EmployeeLevel`.
        * created (models.DateTimeField): The date & time this `EmployeeLevel` was
            created.
        * modified (models.DateTimeField): The date & time this `EmployeeLevel` was last
            modified.
    """

    level: models.PositiveIntegerField = models.PositiveIntegerField(
        unique=True, editable=False
    )

    def __str__(self) -> str:
        """String Representation of `EmployeeLevel`."""

        return f"EmployeeLevel(id={self.id}, name={self.name}, level={self.level})"

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for EmployeeLevel."""

        db_table_comment = ""
        default_related_name = "employeelevels"
        indexes = [
            models.Index(fields=("level",), name="employeelevel_level"),
            models.Index(fields=("name",), name="employeelevel_name"),
            models.Index(fields=("id",), name="employeelevel_id"),
        ]
        ordering = ["level"]
        verbose_name = "employee level"
        verbose_name_plural = "employee levels"


EmployeeLevel.Meta.db_table_comment = EmployeeLevel.__doc__  # type: ignore[assignment]
