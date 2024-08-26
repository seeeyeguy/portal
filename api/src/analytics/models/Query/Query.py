"""
`Query` represents a search for a resource by a user.
Each search committed by users is stored with our
`Query` model. `Query` consists of user(`User`), search_term(str),
and a created time(datetime). With `Query`, we can provide
functionality such as search suggestions, auto-complete,
preferred resource ordering, data analytics, etc. And thus,
we can greatly improve the user experience.
"""

# pylint: disable=no-member
from django.contrib.auth import get_user_model
from django.db import models

from portal.models import DateTimeAbstractModel


class Query(DateTimeAbstractModel):
    """
    `Query` represents a search for a `Resource` by a `User`.
    `Query` provides analytical data for resources so that
    `BI Portal` may provide insights and improve the user's
    experience.

    A `Query` includes:
        * id (int): An auto-generated number managed by the database.
        * user (contrib.auth.models.User): A `BI Portal` user.
        * search_term (models.CharField): A search string submitted by the user.
        * resources (models.ManyToManyField[directory.models.Resource]): A set
            of resources fetched with this query at the time it was created.
        * created (models.DateTimeField): The date & time this `Query` was created.
    """

    user: models.ForeignKey = models.ForeignKey(
        get_user_model(), to_field="username", on_delete=models.CASCADE
    )
    search_term: models.CharField = models.CharField(max_length=512)
    resources: models.ManyToManyField = models.ManyToManyField(
        "directory.Resource", db_table="query_resources"
    )
    modified = None  # type: ignore[assignment]

    def __str__(self) -> str:
        """String Representation of `Query`."""

        return (
            f"Query(id={self.id}, user={self.user.email},"
            f" search_term={self.search_term})"
        )

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `Query`."""

        db_table_comment = ""
        default_related_name = "queries"
        indexes = [
            models.Index(fields=("search_term",), name="query_search_term"),
            models.Index(fields=("user",), name="query_user"),
            models.Index(fields=("id",), name="query_id"),
        ]
        ordering = ["search_term", "-created"]
        verbose_name = "query"
        verbose_name_plural = "queries"


Query.Meta.db_table_comment = Query.__doc__  # type: ignore[assignment]
