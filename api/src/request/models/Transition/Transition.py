""" 
`Transition` models request transitions, tracking a request
as it moves through stages of the request workflow.
"""

# pylint: disable=no-member
from django.db import models

from portal.models import DateTimeAbstractModel


class Transition(DateTimeAbstractModel):
    """
    `Transition` represents the transition of a `Resource`
    from one `Stage` to another. `Resource`s transition from
    their initial `Stage` inevitably to their final `Stage`,
    where a request for an addition or change is ultimately
    approved or rejected.

    A `Transition` includes:
        * id (int): An auto-generated number managed by the database.
        * request (request.models.Request): `Request` that is being tracked.
        * stage (request.models.Stage): The stage of the transition.
        * previous_transition (request.models.Transition): The `Request`'s
            previous `Transition`.
        * created (models.DateTimeField): The date & time this `Transition`
            was created.
    """

    request: models.ForeignKey = models.ForeignKey(
        "request.Request", on_delete=models.PROTECT
    )
    stage: models.ForeignKey = models.ForeignKey(
        "request.Stage", on_delete=models.PROTECT
    )
    previous_transition: models.OneToOneField = models.OneToOneField(
        "self", null=True, on_delete=models.PROTECT
    )
    modified = None  # type: ignore[assignment]

    def __str__(self) -> str:
        """String Representation of `Transition`."""

        previous_stage = (
            self.previous_transition.stage.name if self.previous_transition else None
        )

        return (
            f"Transition(id={self.id}, request={self.request}, stage={self.stage.name},"
            f" previous_stage={previous_stage})"
        )

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `Transition`."""

        db_table_comment = ""
        default_related_name = "transitions"
        indexes = [
            models.Index(fields=["stage"], name="transition_stage"),
            models.Index(fields=["request"], name="transition_request"),
            models.Index(fields=["id"], name="transition_id"),
        ]
        ordering = ["id"]
        verbose_name = "transition"
        verbose_name_plural = "transitions"


Transition.Meta.db_table_comment = Transition.__doc__  # type: ignore[assignment]
