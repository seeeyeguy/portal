"""
`Visit` represents a visit to a resource by a user.
Each visit committed by users is stored with our
`Visit` model. `Visit` consists of user(`User`), resource(`Resource`),
and created time(datetime). `Visit` establishes an indirect
relationship between `User` and `Resource`. A user may have
many visits and a resource can relate to many visits. 
"""

# pylint: disable=no-member
from django.contrib.auth import get_user_model
from django.db import models

from portal.models import DateTimeAbstractModel


class Visit(DateTimeAbstractModel):
    """
    `Visit` represents a visit (click) to a `Resource`.
    `Visit` provides analytical data for resources so that
    `BI Portal` may provide insights and improve the user's
    experience.

    A `Visit` includes:
        * id (int): An auto-generated number managed by the database.
        * user (contrib.auth.models.User): A `BI Portal` user.
        * resource (directory.models.Resource): A visited `Resource`.
        * created (models.DateTimeField): The date & time this `Visit` was created.
    """

    user: models.ForeignKey = models.ForeignKey(
        get_user_model(), to_field="username", on_delete=models.CASCADE
    )
    resource: models.ForeignKey = models.ForeignKey(
        "directory.Resource", on_delete=models.CASCADE
    )
    modified = None  # type: ignore[assignment]

    def __str__(self) -> str:
        """String Representation of `Visit`."""

        return (
            f"Visit(id={self.id}, user={self.user.email},"
            f" resource={self.resource.name})"
        )

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `Visit`."""

        db_table_comment = ""
        default_related_name = "visits"
        indexes = [
            models.Index(fields=("resource",), name="visit_resource"),
            models.Index(fields=("user",), name="visit_user"),
            models.Index(fields=("id",), name="visit_id"),
        ]
        ordering = ["-created"]
        verbose_name = "visit"
        verbose_name_plural = "visits"


Visit.Meta.db_table_comment = Visit.__doc__  # type: ignore[assignment]
