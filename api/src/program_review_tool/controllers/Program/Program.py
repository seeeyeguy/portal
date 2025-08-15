"""
`Program` Controllers module. Controllers permit the addition,
modification, deletion, fetching, and processing of data.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import cast, List, Optional, Tuple

import django_rq
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet

from program_review_tool import controllers, exceptions, models
from program_review_tool.utils.review.export import (
    DEFAULT_EXPORT_ERROR_MESSAGE,
    ExportStatus,
    generate_program_review_powerpoint_wrapper,
    PROGRAM_REVIEW_CACHE_PREFIX,
)
from program_review_tool.utils.review.tableau import (
    get_tableau_token_for_job,
    TABLEAU_AUTH_CACHE_TIMEOUT,
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


class Program:
    """
    Container class for functions related to retrieving
    and reviewing `Program` records.
    """

    @staticmethod
    def fetch_programs(
        program_ids: List[int], page: Optional[int] = None, limit: Optional[int] = None
    ) -> QuerySet[models.Program]:
        """
        Fetch all `Program` records for the given
        ids.

        Accepts:
            * program_ids (List[int]): Primary keys of a set of
                Program records.
            * page (int): The page of `Program` records to return.
            * limit (int): The limit of `Program` records to return.

        Returns:
            * programs (QuerySet[models.Program]): `Program`
                records for the given ids.
        """

        LOGGER.info(f"Fetching Programs with ids: {program_ids}")

        programs = models.Program.objects.filter(active_status=True)

        programs = programs.order_by("id") if page or limit else programs

        # If program ids are given, filter QuerySet to corresponding `Program` records.
        if program_ids:
            programs = programs.filter(id__in=program_ids)
            # If some programs ids not in `Program` QuerySet, throw an error.
            if programs.count() != len(program_ids):
                missing_program_ids = set(program_ids) - set(
                    programs.values_list("id", flat=True)
                )
                raise exceptions.ProgramReviewToolError(
                    f"Programs(ids={missing_program_ids}) do not exist.", 404
                )

        # If `limit` is given, then limit the `Program` records.
        programs = programs[:limit] if limit else programs

        if page:
            # Create a Paginator to paginate the collection
            # of `Program`s.
            paginator: Paginator = Paginator(programs, DEFAULT_PAGE_LENGTH)

            # If `page` number supplied in the params is greater
            # than the number of available pages, then return an
            # empty `Program` Queryset.
            if page > paginator.num_pages:
                return models.Program.objects.none()

            # Get the corresponding Page.
            program_page: Page = paginator.page(page)

            # Assign the page's `Program` QuerySet to
            # `programs`.
            programs = cast(QuerySet[models.Program], program_page.object_list)

        return programs

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
        user_email: str = user.email
        # Create a list of sorted `Program` ids.
        sorted_programs_ids = sorted(program_ids)
        # Construct string of `Program ids`.
        program_ids_str: str = "-".join([str(p_id) for p_id in sorted_programs_ids])

        # Construct cache key to track the export job for this user, review name,
        # and `Program` ids.
        export_cache_key: str = f"{PROGRAM_REVIEW_CACHE_PREFIX}_{user_email}_{review_name}_{program_ids_str}"

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
        programs: QuerySet[models.Program] = models.Program.objects.filter(
            id__in=program_ids, active_status=True
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

        # Set period for export from the current time.
        period: str = datetime.now().strftime("%Y%m")

        # Construct the reviewer name from the first and last name
        # of the `User`.
        reviewer_name: str = f"{user.first_name} {user.last_name}"

        # Retrieve a Tableau token and its cache key.
        tableau_token_cache_key, tableau_token_for_job = get_tableau_token_for_job()

        # If there is no token then raise an error.
        if not tableau_token_for_job:
            err_msg = "Export generation service is overloaded. Please try again later."
            raise exceptions.ProgramReviewToolError(err_msg, 529)

        # Set the retrieved token as 'in use'.
        cache.set(
            tableau_token_cache_key,
            (tableau_token_for_job, True),
            TABLEAU_AUTH_CACHE_TIMEOUT,
        )

        # Create `Usage` entry for export job.
        usage = controllers.Usage.create_usage(user_email, pa_numbers)

        # Get the scheduler and queue the job for
        # generating the PowerPoint export.
        scheduler = django_rq.get_scheduler("default")
        scheduler.enqueue_in(
            timedelta(seconds=5),
            generate_program_review_powerpoint_wrapper,
            pa_numbers,
            period,
            reviewer_name,
            review_name,
            export_cache_key,
            tableau_token_cache_key,
            tableau_token_for_job,
            usage.id,
            meta={
                "job_name": PROGRAM_REVIEW_EXPORT_JOB_NAME,
                "cache_key": export_cache_key,
            },
        )

        # Set the `Queued` status for the export_cache_key.
        cache.set(export_cache_key, (ExportStatus.QUEUED, None))
        return (ExportStatus.QUEUED, None)
