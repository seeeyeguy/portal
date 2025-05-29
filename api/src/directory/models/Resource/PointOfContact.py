"""
`PointOfContact` represent a relationship between `Resource`
and `User` records. `PointOfContact` records denotes who
are the primary and secondary point of contacts for a `Resource`
record. It references who a user may contact to solicit more
information regarding a resource.
"""

from django.db import models


class PointOfContact(models.Model):
    """
    `PointOfContact` represents a relationship between `Resource`
    and `User`. These records confer who a `User` may contact
    to solicit more information about a `Resource`.

    A `PointOfContact` includes:
        * id (int): An auto-generated number managed by the database.
        * resource (directory.Resource): A directory `Resource`.
        * contact (auth.User): A `User` who may be contacted for
            more information regarding a resource.
        * primary (bool): Whether the related `User` is a primary or
            secondary point of contact.
    """

    resource = models.ForeignKey("directory.Resource", on_delete=models.CASCADE)
    contact = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    primary = models.BooleanField(null=True, default=None)

    def __str__(self) -> str:
        """String Representation of `PointOfContact`."""

        return f"PointOfContact(resource={self.resource}, contact={self.contact})"

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `PointOfContact`."""

        default_related_name = "pointofcontacts"

        constraints = [
            models.UniqueConstraint(
                fields=["resource", "contact"], name="resource_contact_id"
            )
        ]

        verbose_name = "point of contact"
        verbose_name_plural = "point of contacts"
