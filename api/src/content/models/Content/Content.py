"""
`Content` represents dynamic content that may
appear in `BI Portal`'s UI. With the `Content` model,
site admins can create and manage generic/dynamic
content that may provide helpful information to
application users. A `Content` content is a
JSON object associated with a key that helps
identify the purpose of that content.
"""

from django.contrib.auth import get_user_model
from django.db import models

from portal.models import DateTimeAbstractModel


class Content(DateTimeAbstractModel):
    """
    `Content` represent dynamic content that may appear
    in `BI Portal`'s UI.

    A `Content` instance includes:
      * id (int): An auto-generated number managed by the database.
      * key (models.CharField): An alias for dynamic content.
      * content (models.JSONField): Dynamic content for `BI Portal`.
      * created (models.DateTimeField): The date & time this `Content` was created.
      * modified (models.DateTimeField): The date & time this `Content` was modified.
      * modified_by (contrib.auth.models.User): A `BI Portal` user.
    """

    key = models.CharField(max_length=512, unique=True)
    content = models.JSONField()
    modified_by = models.ForeignKey(
        get_user_model(), to_field="username", null=True, on_delete=models.SET_NULL
    )

    def __str__(self) -> str:
        """String Representation of `Content`."""

        return f"Content(id={self.id}, key={self.key}, content={self.content})"

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `Content`."""

        db_table_comment = ""
        default_related_name = "content"
        indexes = [
            models.Index(fields=("key",), name="content_key"),
            models.Index(fields=("id",), name="content_id"),
        ]
        ordering = ["-modified"]
        verbose_name = "content"
