"""
`Program` Controllers module. Controllers permit the addition,
modification, deletion, fetching, and processing of data.

Updated to use PowerBI API instead of Tableau.
"""

import logging
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import cast, List, Optional, Set, Tuple

import django_rq
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.db.models.functions import Lower, Trim

from program_review_tool import controllers, exceptions, models
from program_review_tool.utils.review.export import (
    DEFAULT_EXPORT_ERROR_MESSAGE,
    ExportStatus,
    generate_program_review_powerpoint_wrapper,
    PROGRAM_REVIEW_CACHE_PREFIX,
)
from program_review_tool.utils.review.powerbi.config import (
    AZURE_TOKEN_CACHE_KEY,
)
from program_review_tool.utils.review.powerbi.scripts.authenticate_with_powerbi import (
    get_powerbi_token_for_job,
)

from manager.settings import ApplicationBuild, BUILD

LOGGER = logging.getLogger(__name__)


# Default page length used when using
# pagination on the search.
DEFAULT_PAGE_LENGTH: int = 50

# Program review export job name.
PROGRAM_REVIEW_EXPORT_JOB_NAME: str = "program_review_export"

# Program review export job cache missing/expired string.
EXPORT_JOB_CACHE_EXPIRED_TEXT: str = "no_program_review_export_job_found"

# Program review export job cache value set when in queue.
EXPORT_JOB_CACHE_QUEUED_TEXT: str = "program_review_export_job_queued"

# Azure AD token cache timeout (1 hour minus 10% for safety)
AZURE_AUTH_CACHE_TIMEOUT: int = int(os.getenv("AZURE_AUTH_CACHE_TIMEOUT", 3240))


class Program:
    """
    Container class for functions related to retrieving
    and reviewing `Program` records.
    """

    @staticmethod
    def fetch_programs(
        program_ids: List[int],
        pa_numbers: List[str],
        tiers: List[int] = [],
        segments: List[int] = [],
        program_member: str = "",
        active_only: bool = True,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> QuerySet[models.Program]:
        """
        Fetch all `Program` records for the given
        ids, PA numbers, tiers and/or program member.

        Accepts:
            * program_ids (List[int]): Primary keys of a set of
                Program records.
            * pa_numbers (List[str]): PA Numbers of a set of
                Program records.
            * tiers (List[int]): Tiers of the `Program`
                records to return.
            * segments (List[int]): Segments of the `Program`
                records to return.
            * program_member (str): E-mail of the `User` with
                active `ProgramMember` records associated with
                the `Program` records to return.
            * page (int): The page of `Program` records to return.
            * limit (int): The limit of `Program` records to return.

        Returns:
            * programs (QuerySet[models.Program]): `Program`
                records for the given ids, PA numbers, tiers and/or
                program member.
        """
        try:
            # If both program ids and PA numbers are given, throw an error.
            if program_ids and pa_numbers:
                err_msg = (
                    f"Can't fetch Programs by ids (ids:{program_ids}) "
                    f"and PA numbers (pa_numbers:{pa_numbers})."
                )
                LOGGER.error(err_msg)
                raise exceptions.ProgramReviewToolError(err_msg, 400)

            info_log_msg: str = "Fetching Programs"
            info_log_msg = (
                f"{info_log_msg} with ids:{program_ids}"
                if program_ids
                else info_log_msg
            )
            info_log_msg = (
                f"{info_log_msg} with PA Numbers: {pa_numbers}"
                if pa_numbers
                else info_log_msg
            )
            info_log_msg = (
                f"{info_log_msg}, by tiers: {tiers}" if tiers else info_log_msg
            )
            info_log_msg = (
                f"{info_log_msg}, by segments: {segments}" if segments else info_log_msg
            )
            info_log_msg = (
                f"{info_log_msg}, by Program Member: {program_member}"
                if program_member
                else info_log_msg
            )
            info_log_msg = (
                f"{info_log_msg}, with limit: {limit}" if limit else info_log_msg
            )
            info_log_msg = f"{info_log_msg}, for page: {page}" if page else info_log_msg

            LOGGER.info(info_log_msg)

            if active_only:
                programs = cast(
                    QuerySet[models.Program],
                    models.Program.objects.filter(active_status=True),
                )
            else:
                programs = cast(
                    QuerySet[models.Program],
                    models.Program.objects.all(),
                )

            programs = programs.order_by("id") if page or limit else programs

            # If program ids are given, filter the QuerySet to corresponding `Program` records.
            if program_ids:
                programs = programs.filter(id__in=program_ids)
                # If some `Program`s with ids not in `Program` QuerySet, throw an error.
                if programs.count() != len(program_ids):
                    missing_programs_program_ids = set(program_ids) - set(
                        programs.values_list("id", flat=True)
                    )
                    raise exceptions.ProgramReviewToolError(
                        f"Programs(ids={missing_programs_program_ids}) do not exist.",
                        404,
                    )

            # If PA numbers are given, filter the QuerySet to corresponding `Program` records.
            if pa_numbers:
                lowered_pa_numbers = [pa.lower().strip() for pa in pa_numbers]

                programs = (
                    programs.annotate(_pa_clean=Lower(Trim("pa_number")))
                    .filter(_pa_clean__in=lowered_pa_numbers)
                    .order_by("id")
                )

                # If some `Program`s with PA numbers not in `Program` QuerySet, throw an error.
                if programs.count() != len(pa_numbers):
                    missing_programs_pa_numbers = set(lowered_pa_numbers) - set(
                        programs.values_list("_pa_clean", flat=True)
                    )
                    raise exceptions.ProgramReviewToolError(
                        f"Programs(pa_numbers={missing_programs_pa_numbers}) do not exist.",
                        404,
                    )

            # If program tiers are given, filter QuerySet to corresponding `Program` records.
            if tiers:
                programs = programs.filter(tier__in=tiers)

            # If program segments are given, filter QuerySet to corresponding `Program` records.
            if segments:
                programs = programs.filter(segment__id__in=segments)

            # If a `ProgramMember` `User` e-mail is given, filter the QuerySet to corresponding
            # `Program` records in which the `User` has associated active `ProgramMember` entries.
            if program_member:
                # Fetch related `User` record.
                program_member_user_record = User.objects.using("prt").get(
                    email__iexact=program_member
                )
                # Create set of `Program` ids for which the `User` has associated active
                # `ProgramMember` entries.
                program_member_program_ids: Set[int] = set(
                    models.ProgramMember.objects.filter(
                        user=program_member_user_record,
                        expiry_date__isnull=True,
                    ).values_list("program__id", flat=True)
                )

                programs = programs.filter(id__in=program_member_program_ids)

            if page:
                # Use limit if provided, otherwise use DEFAULT_PAGE_LENGTH
                page_length = limit if limit else DEFAULT_PAGE_LENGTH

                # Create a Paginator to paginate the collection of `Program`s.
                paginator: Paginator = Paginator(programs, page_length)

                # If `page` number supplied in the params is greater than the number of available pages,
                # then return an empty `Program` Queryset.
                if page > paginator.num_pages:
                    return cast(QuerySet[models.Program], models.Program.objects.none())

                # Get the corresponding Page.
                program_page: Page = paginator.page(page)
                # Assign the page's QuerySet to our return value.
                programs = cast(QuerySet[models.Program], program_page.object_list)
            elif limit:
                # If no page is provided but limit is provided, limit the `Program` records.
                programs = programs[:limit]

            return programs
        except User.DoesNotExist as exc:
            err_msg = f"User (username={program_member}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404) from exc

    @staticmethod
    def review_programs(
        program_ids: List[int], user: User, review_name: str
    ) -> Tuple[int, Optional[str]]:
        """
        Reviews the `Program` records for the given
        ids, generates the review PowerPoint export and
        returns its path.

        Accepts:
            * program_ids (List[int]): Primary keys of a set of
                Program records.
            * user (User): The user who requested the review.
            * review_name (str): The name of the review.

        Returns:
            * program_review_export_status (int): A numerical representation
                indicating the status of the export job. Status values:
                    * Failure = -1
                    * Queued = 0
                    * In-Progress = 1
                    * Done = 2
            * export_path (str): Path of the review PowerPoint
                export generated.
        """

        LOGGER.info(f"Reviewing Programs with ids: {program_ids}")

        if not program_ids:
            err_msg = "No Program ids given to review."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 400)

        if not review_name.strip():
            err_msg = "No name given for the review."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 400)

        # Get the user's email.
        user_username: str = user.username
        # Create a list of sorted `Program` ids.
        sorted_programs_ids = sorted(program_ids)
        # Construct string of `Program ids`.
        program_ids_str: str = "-".join([str(p_id) for p_id in sorted_programs_ids])

        # Construct cache key to track the export job for this user, review name,
        # and `Program` ids.
        export_cache_key: str = f"{PROGRAM_REVIEW_CACHE_PREFIX}_{user_username}_{review_name}_{program_ids_str}"

        # Query the cache by the export_cache_key for the
        # export's status and value (either the export's path or
        # an error message in the event of failure).
        program_review_export_status, export_value = cache.get(
            export_cache_key, (None, None)
        )

        # If the status is `Queued` or `In-Progress`,
        # return the status and export path (will be None).
        if program_review_export_status in {
            ExportStatus.QUEUED,
            ExportStatus.IN_PROGRESS,
        }:
            return (program_review_export_status, export_value)

        # If the status is `Done`, proceed to evaluate further.
        if program_review_export_status == ExportStatus.DONE:
            export_path = export_value
            # If the path is not None and the path to the file
            # exists, return the status and the export path.
            if export_path is not None and os.path.exists(export_path):
                return (program_review_export_status, export_path)
            # Else, set status to `Failed` and update the cache
            # entry.
            program_review_export_status = ExportStatus.FAILED
            cache.set(
                export_cache_key, (ExportStatus.FAILED, DEFAULT_EXPORT_ERROR_MESSAGE)
            )

        # If status is `Failed`, log an error and raise an exception.
        if program_review_export_status == ExportStatus.FAILED:
            err_msg = export_value
            LOGGER.error(err_msg)
            error_code = 500 if err_msg == DEFAULT_EXPORT_ERROR_MESSAGE else 529
            raise exceptions.ProgramReviewToolError(err_msg, error_code)

        # Fetch active `Program`s that match the given ids.
        programs: QuerySet[models.Program] = cast(
            QuerySet[models.Program],
            models.Program.objects.filter(id__in=program_ids),
        )

        # Verify that number of retrieved `Program`s is equal
        # to the number of ids given.
        if programs.count() != len(program_ids):
            err_msg = f"Some Programs (ids={program_ids}) do not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404)

        # If `BUILD` is `test` then return a `Queued`
        # response.
        if BUILD == ApplicationBuild.TEST:
            return (ExportStatus.QUEUED, None)

        # Construct a list of pa numbers from the fetched `Program`s.
        pa_numbers: List[str] = list(programs.values_list("pa_number", flat=True))

        # Fetch the program managers from `ProgramMember` based on pa_numbers.
        program_managers = list(
            models.ProgramMember.objects.filter(
                program__pa_number__in=pa_numbers,
                role__id=models.ProgramRole.ProgramRoles.PROGRAM_MANAGER,
            ).values("user__first_name", "user__last_name")
        )

        program_manager_names_list = [
            f"{name['user__first_name']} {name['user__last_name']}"
            for name in program_managers
        ]

        program_manager_names = ", ".join(program_manager_names_list)

        # Set the reporting period for the export to the previous reporting period
        period: str = (datetime.now() - relativedelta(months=1)).strftime("%Y%m")

        # Retrieve a PowerBI token and its cache key.
        powerbi_token_cache_key, powerbi_token_for_job = get_powerbi_token_for_job()

        # If there is no token then raise an error.
        if not powerbi_token_for_job:
            err_msg = "Export generation service is overloaded. Please try again later."
            raise exceptions.ProgramReviewToolError(err_msg, 529)

        # Set the retrieved token as 'in use'.
        cache.set(
            powerbi_token_cache_key,
            (powerbi_token_for_job, True),
            AZURE_AUTH_CACHE_TIMEOUT,
        )

        # Create `Usage` entry for export job.
        usage = controllers.Usage.create_usage(user_username, pa_numbers)

        # Get the scheduler and queue the job for
        # generating the PowerPoint export.
        scheduler = django_rq.get_scheduler("default")
        scheduler.enqueue_in(
            timedelta(seconds=5),
            generate_program_review_powerpoint_wrapper,
            pa_numbers,
            period,
            program_manager_names,
            review_name,
            export_cache_key,
            powerbi_token_cache_key,
            powerbi_token_for_job,
            usage.id,
            meta={
                "job_name": PROGRAM_REVIEW_EXPORT_JOB_NAME,
                "cache_key": export_cache_key,
            },
        )

        # Set the `Queued` status for the export_cache_key.
        cache.set(export_cache_key, (ExportStatus.QUEUED, None))
        return (ExportStatus.QUEUED, None)