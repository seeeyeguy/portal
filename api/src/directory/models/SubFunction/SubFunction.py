"""
`SubFunction` represents a specialized division
within a `Function` that focuses on a more
specific area of expertise. `SubFunction`s are
strictly defined, consisting of name(str),
and description(str). A `SubFunction` can only be
related to a single `Function`, but can be related
to many different `Resource`s. `SubFunction` fosters
an indirect relationship between `Resource` and `Function`
as well as divides `Resource`s into discrete groups
within a `Function`.
"""

from django.db import models

from portal.models import BasicInformationAbstractModel, DateTimeAbstractModel


class SubFunction(BasicInformationAbstractModel, DateTimeAbstractModel):
    """
    `SubFunction` represents a specialized division within a `Function`
    that focuses on a more specific area of expertise. SubFunctions help
    to classify a resource, and provide metadata. SubFunctions are a strictly
    defined set created by a superuser.

    A `SubFunction` includes:
        * id (int): An auto-generated number managed by the database.
        * name (models.CharField): The name of the `SubFunction`.
        * description (models.CharField): A short/detailed description of what
            this `SubFunction` is.
        * function (directory.models.Function): The `Function` that this `SubFunction`
            relates to.
        * created (models.DateTimeField): The date & time this `SubFunction` was created.
        * modified (models.DateTimeField): The date & time this `SubFunction` was last
            modified.
    """

    function: models.ForeignKey = models.ForeignKey(
        "directory.Function", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        """String Representation of `SubFunction`."""

        return f"SubFunction(id={self.id}, name={self.name})"

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for SubFunction."""

        db_table_comment = ""
        default_related_name = "subfunctions"
        indexes = [
            models.Index(fields=("function",), name="subfunction_function"),
            models.Index(fields=("name",), name="subfunction_name"),
            models.Index(fields=("id",), name="subfunction_id"),
        ]
        ordering = ["name"]
        verbose_name = "subfunction"
        verbose_name_plural = "subfunctions"


SubFunction.Meta.db_table_comment = SubFunction.__doc__  # type: ignore[assignment]
