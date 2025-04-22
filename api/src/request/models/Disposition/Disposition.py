"""
`Disposition` represents a vote by a BI Portal admin on a
request to add/modify a directory resource. A request must
have all needed dispositions before it can transition to the
next stage (state) in the request workflow. `Disposition` can be
`APPROVED`, `REJECTED`, `REVISE`, etc. A disposition is final and
cannot be modified. `Disposition`s should never be deleted without
an appropriate reason. `Disposition`s also help provide validation
for a request and thus additions/changes to directory resources.
"""

# pylint: disable=no-member
from django.db import models

from portal.models import DateTimeAbstractModel


class Disposition(DateTimeAbstractModel):
    """
    `Disposition` represents a vote by a BI Portal admin
    on a request to add/modify a directory resource. `Resource`s
    transition from their initial `Stage` inevitably to their
    final `Stage`, where a request for an addition or change is
    ultimately approved or rejected. Dispositions are the primary
    catalyst for such transitions. Once a request receives sufficient
    dispositions, a request transitions to its next stage. `Disposition`s
    should never be deleted.

    A `Disposition` includes:
        * id (int): An auto-generated number managed by the database.
        * approver (users.models.Access): Access of the BI Portal admin
            that voted.
        * disposition (models.CharField): A vote for a request.
        * justification (models.TextField): A reason as to why a vote was
            ultimately made.
        * transition (request.models.Transition): The related `Transition`
            for this `Disposition`.
        * created (models.DateTimeField): The date & time this `Disposition`
            was created.
    """

    # pylint: disable=too-few-public-methods
    class DispositionValues:
        """Supported values for `Disposition`s."""

        APPROVED = "APPROVED"
        REJECTED = "REJECTED"
        REVISE = "REVISE"

    approver: models.ForeignKey = models.ForeignKey(
        "users.Access", on_delete=models.PROTECT
    )
    disposition: models.CharField = models.CharField(max_length=512)
    justification: models.TextField = models.TextField(blank=True)
    transition: models.ForeignKey = models.ForeignKey(
        "request.Transition", on_delete=models.PROTECT
    )
    modified = None  # type: ignore[assignment]

    def __str__(self) -> str:
        """String Representation of `Disposition`."""

        return (
            f"Disposition(id={self.id}, approver={self.approver.user.email},"
            f" disposition={self.disposition}, transition={self.transition.stage.name})"
        )

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `Disposition`."""

        db_table_comment = ""
        default_related_name = "dispositions"
        indexes = [
            models.Index(fields=["transition"], name="disposition_transition"),
            models.Index(fields=["disposition"], name="disposition_disposition"),
            models.Index(fields=["approver"], name="disposition_approver"),
            models.Index(fields=["id"], name="disposition_id"),
        ]
        ordering = ["approver", "transition"]
        verbose_name = "disposition"
        verbose_name_plural = "dispositions"


Disposition.Meta.db_table_comment = Disposition.__doc__  # type: ignore[assignment]
