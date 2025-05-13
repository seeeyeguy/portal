"""
`BI Portal` `Access` controller module. Controllers
create, fetch, and update records within the `Access`
table. `Access` represents a relationship between a `User`
and a `Role`, thus conferring system permissions and
access to that user. More specifically, an `Access`
may help determine whether a `User` can create, update
and/or approve a `Resource` `Request` in the request
workflow. A `Resource` `Request` must be created
by a `User` with an appropriate `Access` in the system
and ultimately approved by a `User` with an appropriate
`Access`.
"""

from typing import List, Optional, Tuple

from django.contrib.auth import models as AuthModels
from django.db.models import QuerySet

from users import models


class Access:
    """
    Container class for functions related to creating, updating,
    and retrieving `Access` records. `Access` represents a
    relationship between a `User` and a `Role`, thus conferring
    system permissions and access to that user within `BI Portal`.
    """

    @staticmethod
    def create_access(
        user: str,
        role_level: int,
        subfunctions: Optional[List[int]],
        stage_levels: Optional[List[int]],
        admin: AuthModels.User,
    ) -> models.Access:
        """
        Create an `Access` for the given `User`, with the given role
        with permissions for the given subfunctions and stages.

        Accepts:
            * user (str): An valid email to reference a `BI Portal` user.
            * role_level (int): The level for the related `Role`.
            * subfunctions (List[int]): A list of ids for `Subfunction`s
                for which this access may submit a request or disposition.
            * stage_levels (List[int]): A list of levels for `Stage`s for which
                this access may submit a disposition.
            * admin (auth.AuthModels.User): A `BI Portal` user that made the request.
                This `User` must have an `Access` with the role `Superuser`.

        Returns:
            * access (models.Access): A new `Access` record for the given user.
        """

        return models.Access()

    @staticmethod
    def revoke_access(access: int, admin: AuthModels.User) -> Tuple[models.Access, int]:
        """
        Revoke an `Access` if and only if the requesting admin has appropriate permissions.

        Accepts:
            * access (int): An id for a valid `Access` record.
            * admin (auth.AuthModels.User): A `BI Portal` user that made the request.
                This `User` must have an `Access` with the role `Superuser`.

        Returns:
            * access (models.Access): An updated `Access` record for the given user.
            * rows_affected (int): The number of records affected.
        """

        return models.Access(), 1

    @staticmethod
    def fetch_accesses(
        access: Optional[int],
        user: Optional[str],
        role_levels: Optional[List[int]],
        subfunctions: Optional[List[int]],
        include_revoked: Optional[bool],
        admin: AuthModels.User,
    ) -> QuerySet[models.Access]:
        """
        Fetch an `Access` record, given its id. If an id is not given,
        fetch all `Access` records, filtering by `user`, `role_levels`
        and/or `subfunctions` as appropriate. May include revoked `Access`
        records.

        Accepts:
            * access (int): An id for an `Access` record.
            * user (str): A valid email to reference a `BI Portal` user to filter
                `Access` records.
            * role_levels (List[int]): A list of role levels to filter `Access` records.
            * subfunctions (List[int]): A list of subfunction ids to filter `Access` records.
            * include_revoked (bool): Whether to include revoked `Access` records.
            * admin (auth.AuthModels.User):  A `BI Portal` user that made the request.
                This `User` must have an `Access` with the role `Superuser`.

        Returns:
            * accesses (Union[models.Access, QuerySet[models.Access]]): An instance or
                queryset of `Access` records, filtered by the given params.
        """

        return models.Access.objects.all()
