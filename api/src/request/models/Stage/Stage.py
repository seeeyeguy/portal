"""
`Stage` models a request workflow stage. A workflow stage represents
the state of a request. If a request transitions from its initial
state to a final state, it is conveyed a status (`APPROVED`,
`REJECTED`, etc) and affirms whether an addition/modification
of a directory resource was accepted.
"""

from django.db import models

from portal.models import BasicInformationAbstractModel


class Stage(BasicInformationAbstractModel):
    """
    `Stage` represents a single phase in the resource request
    workflow. These stages help to determine the progression
    of a `Resource` through that workflow, and thus along
    with `Transition`s permits a `Resource` to be added,
    modified or potentially deleted.

    A `Stage` includes:
        * id (int): An auto-generated number managed by the database.
        * name (models.CharField): Name of the stage.
        * description (models.TextField): Description of the stage.
        * level (models.PositiveIntegerField): An immutable numerical
            representation of the stage.
    """

    class StageLevels:
        """Levels for all `Stage`s in the BI Portal workflow."""

        DRAFT = 1
        SUBMITTED = 2
        APPROVED_BY_BUSINESS_PROCESS_EXPERT = 3
        REVISE = 4
        REJECTED_BY_BUSINESS_PROCESS_EXPERT = 5
        APPROVED_BY_SUPERUSER = 99
        REJECTED_BY_SUPERUSER = 100

        ADJACENCY_LIST = {
            str(REJECTED_BY_SUPERUSER): [
                SUBMITTED,
                APPROVED_BY_BUSINESS_PROCESS_EXPERT,
            ],
            str(APPROVED_BY_SUPERUSER): [
                SUBMITTED,
                APPROVED_BY_BUSINESS_PROCESS_EXPERT,
            ],
            str(REJECTED_BY_BUSINESS_PROCESS_EXPERT): [SUBMITTED],
            str(REVISE): [
                SUBMITTED,
                APPROVED_BY_BUSINESS_PROCESS_EXPERT,
            ],
            str(APPROVED_BY_BUSINESS_PROCESS_EXPERT): [SUBMITTED],
            str(SUBMITTED): [DRAFT],
            str(DRAFT): [None, REVISE],
        }

    level: models.IntegerField = models.PositiveIntegerField(unique=True)

    def __str__(self) -> str:
        """String Representation of `Stage`."""

        return f"Stage(id={self.id}, name={self.name}, level={self.level})"

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `Stage`."""

        db_table_comment = ""
        default_related_name = "stages"
        indexes = [
            models.Index(fields=["level"], name="stage_level"),
            models.Index(fields=["name"], name="stage_name"),
            models.Index(fields=["id"], name="stage_id"),
        ]
        ordering = ["level"]
        verbose_name = "stage"
        verbose_name_plural = "stages"


Stage.Meta.db_table_comment = Stage.__doc__  # type: ignore[assignment]
