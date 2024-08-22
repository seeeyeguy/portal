"""
`Role` represents a role in the system. Roles
are used with accesses to confer permissions &
access to users within the system. Roles are
strictly defined by the system's stakeholders
and instantiated by the development team.
`Role` has a one-to-many relationship with `Access`,
which a has a one-to-many relationship with `User` and
thus we can use this architecture to create a role-based
access control system as a component of our data security,
granting users many roles within the larger system.
"""

from django.db import models

from portal.models import DateTimeAbstractModel


class Role(DateTimeAbstractModel):
    """
    `Role` represents an access role in the system. Access
    roles are used in role-based authorization to determine
    permissions within the application. A `Role` either has
    all permissions for that role or none.

    A `Role` includes:
        * id (int): An auto-generated number managed by the database.
        * name (models.CharField): Name of the role.
        * description (models.TextField): A description of the role's
            purpose and authority.
        * level (models.PositiveIntegerField): An immutable numerical
            representation of that authority.
        * created (models.DateTimeField): The date & time this `Role`
            was created.
    """

    name: models.CharField = models.CharField(unique=True, max_length=512)
    description: models.TextField = models.TextField()
    level: models.PositiveIntegerField = models.PositiveIntegerField(unique=True)
    modified = None  # type: ignore[assignment]

    def __str__(self) -> str:
        """String Representation of `Role`."""

        return (
            f"Role(id={self.id}, name={self.name},"
            f" description={self.description}, level={self.level})"
        )

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `Role`."""

        db_table_comment = ""
        default_related_name = "roles"
        indexes = [
            models.Index(fields=["level"], name="role_level"),
            models.Index(fields=["name"], name="role_name"),
            models.Index(fields=["id"], name="role_id"),
        ]
        ordering = ["level"]
        verbose_name = "role"
        verbose_name_plural = "roles"


Role.Meta.db_table_comment = Role.__doc__  # type: ignore[assignment]
