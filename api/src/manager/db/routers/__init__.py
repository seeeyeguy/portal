"""
Database Routers for Project.
"""

# pylint: disable=protected-access
from typing import Union

from manager.utils.types.model import DjangoModelType


class ProgramReviewToolDatabaseRouter:
    """
    A router to control all database operations on models
    within the `Program Review Tool` app.
    """

    prt_app_label: str = "program_review_tool"

    def db_for_read(self, model: DjangoModelType, **_: dict) -> Union[str, None]:
        """
        Attempts to read apps in `Program Review Tool` go to `prt`.
        """

        if model._meta.app_label == self.prt_app_label:  # type: ignore[attr-defined]
            return "prt"
        return None

    def db_for_write(self, model: DjangoModelType, **_: dict) -> Union[str, None]:
        """
        Attempts to write apps in `Program Review Tool` go to `prt`.
        """

        if model._meta.app_label == self.prt_app_label:  # type: ignore[attr-defined]
            return "prt"
        return None

    def allow_relation(
        self, obj1: DjangoModelType, obj2: DjangoModelType, **_: dict
    ) -> Union[bool, None]:
        """
        Allow relations if a model within an app in `Program Review Tool`
        is involved.
        """

        if (
            obj1._meta.app_label == self.prt_app_label  # type: ignore[attr-defined]
            or obj2._meta.app_label == self.prt_app_label  # type: ignore[attr-defined]
        ):
            return True
        return None

    def allow_migrate(
        self, db: str, app_label: str, _: Union[str, None] = None, **__: dict
    ) -> Union[bool, None]:
        """
        Make sure apps in `Program Review Tool` only appear in the
        'prt' database.
        """

        if app_label == self.prt_app_label:
            return db == "prt"
        return None
