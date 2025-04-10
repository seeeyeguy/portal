"""
`Program` Controllers module. Controllers permit the addition,
modification, deletion, fetching, and processing of data.
"""

import logging
from typing import List

from django.contrib.auth.models import User
from django.db.models import QuerySet

from program_review_tool import models

LOGGER = logging.getLogger(__name__)


class Program:
    """
    Container class for functions related to retrieving
    and reviewing `Program` records.
    """

    @staticmethod
    def fetch_programs(program_ids: List[int]) -> QuerySet[models.Program]:
        """
        Fetch all `Program` records for the given
        ids.

        Accepts:
            * program_ids (List[int]): Primary keys of a set of
                Program records.

        Returns:
            * programs (QuerySet[models.Program]): `Program`
                records for the given ids.
        """

        LOGGER.info(f"Fetching Programs with ids: {program_ids}")

        # Please remove ignore after implementation.
        return {}  # type: ignore[return-value]

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
