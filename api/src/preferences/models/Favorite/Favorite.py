"""
`Favorite` represent a preferred relationship between a
user and a resource. We can consider these much like
bookmarks in a browser, saved links to be easily visited
later. With `Favorite`, the application can display these
preferred resources to the user in a seamless fashion,
thus improving the user's experience.
"""

# pylint: disable=no-member
from django.contrib.auth import get_user_model
from django.db import models

from portal.models import DateTimeAbstractModel


class Favorite(DateTimeAbstractModel):
    """
    `Favorite` represents a resource favorited by a user.
    A `Favorite` allows a user to quickly access a resource
    through the UI.

    A `Favorite` includes:
        * id (int): An auto-generated number managed by the database.
        * user (contrib.auth.models.User): `User` that has favorited the related
            `Resource`.
        * resource (directory.models.Resource): `Resource` that is being favorited
            by the user.
        * rank (models.PositiveIntegerField): A whole number indicating the
            order of this `Favorite` amongst other favorited resources for the
            related `User`.
        * created (models.DateTimeField): The date & time this `Favorite`
            was created.
    """

    user: models.ForeignKey = models.ForeignKey(
        get_user_model(), to_field="username", on_delete=models.CASCADE
    )
    resource: models.ForeignKey = models.ForeignKey(
        "directory.Resource", on_delete=models.CASCADE
    )
    rank: models.PositiveIntegerField = models.PositiveIntegerField()
    modified = None  # type: ignore[assignment]

    def __str__(self) -> str:
        """String Representation of `Favorite`."""

        return (
            f"Favorite(id={self.id}, user={self.user.email},"
            f" resource={self.resource.name}, rank={self.rank})"
        )

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for `Favorite`."""

        db_table_comment = ""
        default_related_name = "favorites"
        indexes = [
            models.Index(fields=["resource"], name="favorite_resource"),
            models.Index(fields=["user"], name="favorite_user"),
            models.Index(fields=["id"], name="favorite_id"),
        ]
        ordering = ["rank", "-created"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "resource"], name="favorite_resource_for_user"
            ),
            models.UniqueConstraint(
                fields=["user", "rank"], name="rank_for_user_favorite"
            ),
        ]
        verbose_name = "favorite"
        verbose_name_plural = "favorites"


Favorite.Meta.db_table_comment = Favorite.__doc__  # type: ignore[assignment]
