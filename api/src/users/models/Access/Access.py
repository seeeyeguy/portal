"""
`Access` represents a user's role in the system.
`Access` relates a user to a role, thus conferring system
permissions and access to that user. `Access` also stores
and manages access granted and access revoked dates to act
as an archive for accesses granted to the user. A user can
have many accesses, an access may have only one role, and
so a user may have many different roles in the system
through their accesses. 
"""

# pylint: disable=no-member
from django.contrib.auth import get_user_model
from django.db import models


class Access(models.Model):
    """
    `Access` represents an individual access within the
    system associated with a role. The application uses
    accesses as part of its role-based authorization to
    grant permissions and privileges to its users. If an
    access is revoked as indicated by `access_revoked_date`,
    all permissions and privileges are also revoked and this
    record is merely kept for historical purposes.

    An `Access` includes:
        * id (int): An auto-generated number managed by the database.
        * user (contrib.auth.models): BI Portal user.
        * role (users.models.Role): Role of the user which confers system
            permissions and access to the user.
        * access_granted_date (models.DateTimeField): The date & time the user was
            granted access with this particular role.
        * access_revoked_date (models.DateTimeField): The date & time this access was
            revoked for this particular role.
        * stage (models.ManyToManyField[request.models.Stage]): The stage at which
            the user with this `Access` is permitted to submit a `Disposition`.
    """

    user: models.ForeignKey = models.ForeignKey(
        get_user_model(), to_field="username", on_delete=models.PROTECT
    )
    role: models.ForeignKey = models.ForeignKey("users.Role", on_delete=models.PROTECT)
    access_granted_date: models.DateTimeField = models.DateTimeField(
        null=True, default=None
    )
    access_revoked_date: models.DateTimeField = models.DateTimeField(
        null=True, default=None
    )
    stage: models.ManyToManyField = models.ManyToManyField(
        "request.Stage", db_table="users_access_stages"
    )

    def __str__(self) -> str:
        """String Representation of `Access`."""

        return (
            f"Access(id={self.id}, user={self.user.email},"
            f" role={self.role.name}, access_granted_date={self.access_granted_date},"
            f" access_revoked_date={self.access_revoked_date})"
        )

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `Access`."""

        db_table_comment = ""
        default_related_name = "accesses"
        indexes = [
            models.Index(fields=["role"], name="access_role"),
            models.Index(fields=["user"], name="access_user"),
            models.Index(fields=["id"], name="access_id"),
        ]
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "role", "access_granted_date"],
                name="user_access_on_granted_date",
            ),
        ]
        verbose_name = "access"
        verbose_name_plural = "accesses"
