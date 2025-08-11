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

import logging
from requests.exceptions import ConnectionError
from typing import List, Optional, Set, Tuple, Union

from django.contrib.auth import models as AuthModels
from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from directory.models import SubFunction
from request.models import Stage
from users import exceptions, models

from manager.services.ldap.provider.utils import fetch_authorized_employee

LOGGER = logging.getLogger(__name__)

TERMINAL_STAGE_LEVELS: Set[int] = {
    Stage.StageLevels.REJECTED_BY_BUSINESS_PROCESS_EXPERT,
    Stage.StageLevels.APPROVED_BY_SUPERUSER,
    Stage.StageLevels.REJECTED_BY_SUPERUSER,
}

VALID_BUSINESS_PROCESS_EXPERT_STAGE_LEVELS: Set[int] = {Stage.StageLevels.SUBMITTED}

VALID_SUPERUSER_STAGE_LEVELS: Set[int] = {
    Stage.StageLevels.SUBMITTED,
    Stage.StageLevels.APPROVED_BY_BUSINESS_PROCESS_EXPERT,
}

VALID_ROLE_STAGE_LEVELS_MAP: dict = {
    models.Role.RoleLevels.DATA_STEWARD: {},
    models.Role.RoleLevels.BUSINESS_PROCESS_EXPERT: VALID_BUSINESS_PROCESS_EXPERT_STAGE_LEVELS,
    models.Role.RoleLevels.SUPERUSER: VALID_SUPERUSER_STAGE_LEVELS,
}


def _validate_stages_for_role(role_level: int, stages: QuerySet[Stage]) -> None:
    """
    Internal function that validates the `Stage`s provided
    for the given `Role` level. If an invalid `Stage` is provided,
    an exception is raised.

    Accepts:
        * role_level (int): Level of the `Role` used for the validation
            against the `Stage`s.
        * stages (QuerySet[Stage]): `Stage`s that will be validated.

    Returns:
        * None
    """

    # Filter out the valid `Stage`s for the given `Role` level to
    # determine if any invalid `Stage`s are present.
    invalid_stages_for_role: List[int] = list(
        stages.exclude(level__in=VALID_ROLE_STAGE_LEVELS_MAP[role_level]).values_list(
            "level", flat=True
        )
    )

    # If `invalid_stages_for_role` is not empty, raise an exception.
    if invalid_stages_for_role:
        err_msg = (
            f"Invalid Stages (levels={invalid_stages_for_role}) for "
            f"Role (level={role_level})."
        )
        LOGGER.error(err_msg)
        raise exceptions.UsersError(err_msg, 400)


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

        try:

            if not (admin and admin.is_authenticated):
                err_msg = "Authentication required."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 401)

            # Verify the permissions of the `admin`.
            if not models.Access.objects.filter(
                user=admin,
                role__level=models.Role.RoleLevels.SUPERUSER,
                access_revoked_date__isnull=True,
            ).exists():
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 403)

            # Fetch `User` record.
            user_record: Optional[AuthModels.User] = fetch_authorized_employee(user)
            if not user_record:
                raise AuthModels.User.DoesNotExist()

            # Verify the `User` does not have already
            # have an `Access` for the given `role_level`.
            if user_record.accesses.filter(
                role__level=role_level, access_revoked_date__isnull=True
            ).exists():
                err_msg = (
                    f"Access for User(email={user}) & Role(level={role_level}) "
                    "already exists."
                )
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 400)

            # Fetch `Role` record.
            role: models.Role = models.Role.objects.get(level=role_level)

            # If the `role` corresponds to a `Superuser` and subfunctions
            #  were given, raise an exception.
            if role.level == models.Role.RoleLevels.SUPERUSER and subfunctions:
                err_msg = "Superusers do not need subfunctions."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 400)

            # Fetch `SubFunction` records.
            subfunction_records: QuerySet[SubFunction] = SubFunction.objects.filter(
                id__in=subfunctions
            )
            if subfunctions and subfunction_records.count() != len(subfunctions):
                err_msg = f"Some SubFunctions (ids={subfunctions}) do not exist."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 404)

            # Fetch `Stage` records.
            stage_records: QuerySet[Stage] = Stage.objects.filter(
                level__in=stage_levels
            )
            if stage_levels and stage_records.count() != len(stage_levels):
                err_msg = f"Some Stages (levels={stage_levels}) do not exist."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 404)

            # Verify `stage_records` does not contain a terminal `Stage`.
            if stage_records.filter(level__in=TERMINAL_STAGE_LEVELS).exists():
                err_msg = "Terminal Stages are not permitted."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 400)

            # Verify `stage_records` does not contain the `DRAFT` `Stage`.
            if stage_records.filter(level=Stage.StageLevels.DRAFT).exists():
                err_msg = "Draft Stage is not permitted."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 400)

            # Validate the `Stage`s for the `Role`.
            _validate_stages_for_role(
                role_level=role.level,
                stages=stage_records,
            )

            # Create `Access` record.
            access: models.Access = models.Access.objects.create(
                user=user_record,
                role=role,
                access_granted_date=timezone.now(),
            )

            # Add `Stages` and `SubFunctions`.
            access.stage.add(*stage_records)
            access.subfunctions.add(*subfunction_records)

            return access
        except (AuthModels.User.DoesNotExist, ConnectionError) as exc:
            err_msg = f"User (email={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.UsersError(err_msg, 404) from exc
        except models.Role.DoesNotExist as exc:
            err_msg = f"Role (level={role_level}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.UsersError(err_msg, 404) from exc

    @staticmethod
    def modify_access(
        access: int, subfunctions: List[int], admin: AuthModels.User
    ) -> Tuple[models.Access, int]:
        """
        Update an `Access` if and only if the requesting admin has the
        appropriate permissions.

        It is important to note that we are forbidden from updating access
        records directly as this opens the application to a major security risk,
        so instead we will perform a "soft" update to the user's access record
        whereby we revoke the given record and issue a new access with the provided
        subfunctions. It is also important to note that we will only ever allow
        subfunctions to be specified/changed here; we are forbidden from changing
        the role or stages.

        Accepts:
            * access (int): An id for a valid `Access` record.
            * subfunctions (List[int]): A list of ids of `Subfunction`s
                for which this access may submit a request or disposition.
            * admin (auth.AuthModels.User): A `BI Portal` user that made the request.
                This `User` must have an `Access` with the role `Superuser`.

        Returns:
            * access_record (models.Access): A new `Access` record for the given user.
            * rows_affected (int): The number of records affected.
        """

        with transaction.atomic():
            revoked_access_record, rows_affected = Access.revoke_access(
                access=access, admin=admin
            )
            stage_levels = list(
                revoked_access_record.stage.values_list("id", flat=True)
            )
            new_access_record = Access.create_access(
                user=revoked_access_record.user.email,
                role_level=revoked_access_record.role.level,
                subfunctions=subfunctions,
                stage_levels=stage_levels,
                admin=admin,
            )
            return new_access_record, rows_affected

    @staticmethod
    def revoke_access(access: int, admin: AuthModels.User) -> Tuple[models.Access, int]:
        """
        Revoke an `Access` if and only if the requesting admin has appropriate permissions.

        Accepts:
            * access (int): An id for a valid `Access` record.
            * admin (auth.AuthModels.User): A `BI Portal` user that made the request.
                This `User` must have an `Access` with the role `Superuser`.

        Returns:
            * access_record (models.Access): An updated `Access` record for the given user.
            * rows_affected (int): The number of records affected.
        """

        try:

            if not (admin and admin.is_authenticated):
                err_msg = "Authentication required."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 401)

            # Verify the permissions of the `admin`.
            if not models.Access.objects.filter(
                user=admin,
                role__level=models.Role.RoleLevels.SUPERUSER,
                access_revoked_date__isnull=True,
            ).exists():
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 403)

            # Fetch `Access` record.
            access_record: models.Access = models.Access.objects.get(id=access)

            # Verify the `Access` being revoked does not belong
            # to the `admin`.
            if access_record.user.email == admin.email:
                err_msg = "Admins can't revoke one of their accesses."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 400)

            # Revoke the target `Access`.
            rows_affected = models.Access.objects.filter(id=access_record.id).update(
                access_revoked_date=timezone.now()
            )

            access_record.refresh_from_db()

            return access_record, rows_affected
        except models.Access.DoesNotExist as exc:
            err_msg = f"Access (id={access}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.UsersError(err_msg, 404) from exc

    @staticmethod
    def fetch_accesses(
        access: Optional[int],
        user: Optional[str],
        role_levels: Optional[List[int]],
        subfunctions: Optional[List[int]],
        include_revoked: Optional[bool],
        admin: AuthModels.User,
    ) -> Union[models.Access, QuerySet[models.Access]]:
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

        try:
            if not (admin and admin.is_authenticated):
                err_msg = "Authentication required."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 401)

            # Verify the permissions of the `admin`.
            if not models.Access.objects.filter(
                user=admin,
                role__level=models.Role.RoleLevels.SUPERUSER,
                access_revoked_date__isnull=True,
            ).exists():
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.UsersError(err_msg, 403)

            # Fetch `Access`, given an `Access` id.
            if access:
                return models.Access.objects.get(id=access)

            # Fetch `Access` records.
            accesses: QuerySet[models.Access] = models.Access.objects.all()

            # Exclude revoked `Access` records if `include_revoked` not set.
            if not include_revoked:
                accesses = accesses.filter(access_revoked_date__isnull=True)

            # Filter records by `User`, given a `User`'s email.
            if user:
                try:
                    domain_index = user.index("@")
                except IndexError:
                    domain_index = 0
                accesses = accesses.filter(user__email__istartswith=user[:domain_index])

            # Filter records by `Role`, given a set of `role_levels`.
            if role_levels:
                accesses = accesses.filter(role__level__in=role_levels)

            # Filter records by `Subfunction`, given a set of `Subfunction` ids.
            if subfunctions:
                accesses = accesses.filter(subfunctions__id__in=subfunctions).distinct()

            return accesses
        except models.Access.DoesNotExist as exc:
            err_msg = f"Access (id={access}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.UsersError(err_msg, 404) from exc
