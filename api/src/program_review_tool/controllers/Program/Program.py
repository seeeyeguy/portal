"""
`Program` Controllers module. Controllers permit the addition,
modification, deletion, fetching, and processing of data.
"""

import logging
from typing import cast, List, Optional

from django.contrib.auth.models import User
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet

from program_review_tool import exceptions, models

LOGGER = logging.getLogger(__name__)


# Default page length used when using
# pagination on the search.
DEFAULT_PAGE_LENGTH: int = 50


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
        program_ids: List[int], user: User, review_name: str = "Portfolio Review"
    ) -> int:
        """
        Reviews the `Program` records for the given
        ids and queues a CRON job to generate the
        PowerPoint export.

        Accepts:
            * program_ids (List[int]): Primary keys of a set of
                Program records.
            * user (User): The user who requested the review.
            * review_name (str): The name of the review.

        Returns:
            * review_status (int): A number indicating either
                success (0) or failure (1) for a review.
        """

        LOGGER.info(f"Reviewing Programs with ids: {program_ids}")

        return 0
