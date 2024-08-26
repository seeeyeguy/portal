"""
`QueryFilterState` represents a preferred state of the BI Portal.
A user may save a `QueryFilterState` so that the application may
load that state on a later visit. A user may have at most, 1 
`QueryFilterState` stored in the database. A `QueryFilterState`
may be saved manually by the user or automatically when the
application is closed. We can consider it much like saving a
document, where the document is in the state a user left it
when it was last saved.
"""

# pylint: disable=no-member
from django.contrib.auth import get_user_model
from django.db import models

from portal import models as BaseModels


class QueryFilterState(BaseModels.DateTimeAbstractModel):
    """
    `QueryFilterState` represents the stored filtered UI state
    for a user. This database table will store at most, 1
    `QueryFilterState` per user. Once a `QueryFilterState` is
    instantiated for a user it should never be deleted, but only
    modified, unless that user is deleted.

    A `QueryFilterState` includes:
        * id (int): An auto-generated number managed by the database.
        * search (analytics.models.Query): A search query made by the user.
        * user (contrib.auth.models.User): `User` that is related to the stored
            filtered state.
        * functions (models.ManyToManyField[directory.models.Function]): `Function`s
            selected by the user.
        * employee_levels (models.ManyToManyField[directory.models.EmployeeLevel]):
            `EmployeeLevel`s selected by the user.
        * tags (models.ManyToManyField[directory.models.Tag]): `Tag`s for resources
            selected by the user.
        * created (models.DateTimeField): The date & time this `QueryFilterState`
            was created.
        * modified (models.DateTimeField): The date & time this `QueryFilterState`
            was last modified.
    """

    search: models.OneToOneField = models.OneToOneField(
        "analytics.Query", on_delete=models.SET_NULL, null=True
    )
    user: models.OneToOneField = models.OneToOneField(
        get_user_model(), to_field="username", on_delete=models.CASCADE
    )
    functions: models.ManyToManyField = models.ManyToManyField(
        "directory.Function", db_table="preferences_queryfilterstate_functions"
    )
    employee_levels: models.ManyToManyField = models.ManyToManyField(
        "directory.EmployeeLevel",
        db_table="preferences_queryfilterstate_employeelevels",
    )
    tags: models.ManyToManyField = models.ManyToManyField(
        "directory.Tag", db_table="preferences_queryfilterstate_tags"
    )

    def __str__(self) -> str:
        """String Representation of `QueryFilterState`."""

        return f"QueryFilterState(id={self.id}, user={self.user.email})"

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `QueryFilterState`."""

        db_table_comment = ""
        default_related_name = "queryfilterstates"
        indexes = [
            models.Index(fields=["user"], name="queryfilterstate_user"),
            models.Index(fields=["id"], name="queryfilterstate_id"),
        ]
        ordering = ["id"]
        verbose_name = "queryfilterstate"
        verbose_name_plural = "queryfilterstates"


# pylint: disable=line-too-long
QueryFilterState.Meta.db_table_comment = QueryFilterState.__doc__  # type: ignore[assignment]
