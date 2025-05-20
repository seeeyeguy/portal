"""
`Portfolio` represents a collection
of `Program`s that a user may submit for review,
generating a PowerPoint review template that provides
a consolidated insight into the health of the programs.
A `Portfolio` relates a `User` to many `Program`s, where
a `Program` is an effort supported by L3Harris Technologies.
A `User` may have many `Portfolio`s with each, given a name by
that `User`.
"""

from django.contrib.auth import get_user_model
from django.db import models

from portal.models import DateTimeAbstractModel


class Portfolio(DateTimeAbstractModel):
    """
    `Portfolio` represents a collection
    of `Program`s that a user may submit for review,
    generating a PowerPoint review template that provides
    a consolidated insight into the health of the programs.

    A `Portfolio` includes:
        * id (int): An auto-generated number managed by the database.
        * user (auth.User): A `Program Review Tool` user.
        * programs (models.ManyToManyField[program_review_tool.models.Program]):
            A set of `Program`s that relate to this `Portfolio`. `Program`s
            help to provide the primary content of `Program Review Tool`.
        * name (models.CharField): The name of the `Portfolio`.
        * created (models.DateTimeField): The date & time this `Portfolio` was created.
        * modified (models.DateTimeField): The date & time this `Portfolio` was last modified.
    """

    user = models.ForeignKey(
        get_user_model(), to_field="username", on_delete=models.CASCADE
    )
    programs = models.ManyToManyField(
        "program_review_tool.Program", db_table="program_review_tool_portfolio_programs"
    )
    name: models.CharField = models.CharField(max_length=512)

    def __str__(self) -> str:
        """String Representation of a `Portfolio`."""

        return f"Portfolio(id={self.id}, name={self.name}, user={self.user})"

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta Class for `Portfolio`."""

        db_table_comment = ""
        default_related_name = "portfolios"
        indexes = [
            models.Index(fields=("user",), name="portfolio_user"),
            models.Index(fields=("name",), name="portfolio_name"),
            models.Index(fields=("id",), name="portfolio_id"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="portfolio_name_for_user"
            )
        ]
        ordering = ["user", "-created"]
        verbose_name = "portfolio"
        verbose_name_plural = "portfolios"
