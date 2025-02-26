"""
`Request` models a request to add or modify a directory resource. Requests
transition stages as they are considered by appropriate BI Portal admins.
These admins submit dispositions, transitioning a request to its appropriate
stage. Once a request reaches its final stage (state), it is conveyed a status
and the associated directory resource and its changes are approved, or rejected.
`Request` provide validation, ensuring that any additions or modifications to
directory resources were appropriately vetted and approved.
"""

# pylint: disable=no-member
from django.db import models

from portal.models import DateTimeAbstractModel


class Request(DateTimeAbstractModel):
    """
    `Request` represents a request made by a user, to add, modify or
    potentially delete a directory resource. `Resource`s transition
    from their initial `Stage` inevitably to their final `Stage`,
    where a request for an addition or change is ultimately approved
    or rejected. A `Resource` is only visible (active) to a user once
    its associated request has transitioned from its initial stage to
    its final stage where it has been approved.

    A `Request` includes:
        * id (int): An auto-generated number managed by the database.
        * resource (directory.models.Resource): A directory resource.
        * originator (users.models.Access): Access of the user who
            created this `Request`.
        * status (models.CharField): Status of the `Request`.
        * created (models.DateTimeField): The date & time this `Request` was
            created.
        * modified (models.DateTimeField): The date & time this `Request` was
            last modified.
    """

    # pylint: disable=too-few-public-methods
    class RequestStatus:
        """Supported statuses for `Request`s."""

        APPROVED = "APPROVED"
        PENDING = "PENDING"
        REJECTED = "REJECTED"

    resource: models.OneToOneField = models.OneToOneField(
        "directory.Resource", on_delete=models.CASCADE
    )
    originator: models.ForeignKey = models.ForeignKey(
        "users.Access", on_delete=models.CASCADE
    )
    status: models.CharField = models.CharField(max_length=512)

    def __str__(self) -> str:
        """String Representation of `Request`."""

        return (
            f"Request(id={self.id}, resource_id={self.resource.id},"
            f" resource_name={self.resource.name},"
            f" originator={self.originator.user.email},"
            f" status={self.status})"
        )

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `Request`."""

        db_table_comment = ""
        default_related_name = "requests"
        indexes = [
            models.Index(fields=["resource"], name="request_resource"),
            models.Index(fields=["originator"], name="request_originator"),
            models.Index(fields=["id"], name="request_id"),
        ]
        ordering = ["-resource"]
        verbose_name = "request"
        verbose_name_plural = "requests"


Request.Meta.db_table_comment = Request.__doc__  # type: ignore[assignment]
