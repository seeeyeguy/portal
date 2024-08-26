"""
`Tag` represents an arbitrary label, associated with
a resource. A `Tag` may be created by any user with 
admin access, representing some metadata about a
resource. We store these tags with the `Tag` model to
provide validation and eliminate redundancies. A `Tag`
can be associated with many `Resource`s and a `Resource`
may be related to many `Tag`s. This many-to-many relationship
conveys a method of categorizing, grouping, and filtering
resources by their tags.
"""

from django.db import models

from portal.models import DateTimeAbstractModel


class Tag(DateTimeAbstractModel):
    """
    `Tag` represents a keyword, used to classify a resource.
    Tags consist primary of an arbitrary label, created by
    a superuser. Tags provide metadata and additional insight
    about a resource.

    A `Tag` includes:
        * id (int): An auto-generated number managed by the database.
        * label (models.CharField): An arbitrary keyword, created by a superuser.
        * created (models.DateTimeField): The date & time this `Tag` was created.
        * modified (models.DateTimeField): The date & time this `Tag` was last modified.
    """

    label: models.CharField = models.CharField(max_length=1028, unique=True)

    def __str__(self) -> str:
        """String Representation of `Tag`."""

        return f"Tag(id={self.id}, label={self.label})"

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for Tag."""

        db_table_comment = ""
        default_related_name = "tags"
        indexes = [
            models.Index(fields=("label",), name="tag_label"),
            models.Index(fields=("id",), name="tag_id"),
        ]
        ordering = ["label"]
        verbose_name = "tag"
        verbose_name_plural = "tags"


Tag.Meta.db_table_comment = Tag.__doc__  # type: ignore[assignment]
