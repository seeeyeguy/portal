"""
`Function` represents a primary
organizational unit that encompasses a broad area
of expertise and responsibility within the organization.
`Function`s are strictly defined, consisting of name(str),
and description(str). A `Function` can be related to many
`SubFunction`s, however, a `SubFunction` can only relate to
a single `Function` and as `SubFunction` has a many-to-many
relationship with `Resource`, `Function` and `Resource` share
an indirect relationship.
"""

from django.db import models

from portal.models import BasicInformationAbstractModel, DateTimeAbstractModel


class Function(BasicInformationAbstractModel, DateTimeAbstractModel):
    """
    `Function` represents a primary organizational unit that encompasses
    a broad area of expertise and responsibility within the organization.
    Functions help to classify a resource, and provide metadata. Functions
    are a strictly defined set created by a superuser.

    A `Function` includes:
        * id (int): An auto-generated number managed by the database.
        * name (models.CharField): The name of the `Function`.
        * description (models.CharField): A short/detailed description of what
            this `Function` is.
        * created (models.DateTimeField): The date & time this `Function` was created.
        * modified (models.DateTimeField): The date & time this `Function` was last
            modified.
    """

    def __str__(self) -> str:
        """String Representation of `Function`."""

        return f"Function(id={self.id}, name={self.name})"

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for Function."""

        db_table_comment = ""
        default_related_name = "functions"
        indexes = [
            models.Index(fields=("name",), name="function_name"),
            models.Index(fields=("id",), name="function_id"),
        ]
        ordering = ["name"]
        verbose_name = "function"
        verbose_name_plural = "functions"


Function.Meta.db_table_comment = Function.__doc__  # type: ignore[assignment]
