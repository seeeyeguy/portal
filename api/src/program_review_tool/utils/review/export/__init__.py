"""
`Program Review Tool` `Program` review export utils module.
Common functionality for `Program Review Tool` `Program` app
to help with generating the `Program` review PowerPoint export.
"""

# pylint: disable=wrong-import-order
import glob
import logging
import os
import pptx
import shutil
import uuid
from datetime import datetime, timedelta
from pandas import DataFrame
from typing import List

import django_rq
from django.core.cache import cache
from django_rq import job as job_decorator
from django.utils import timezone

from program_review_tool import controllers
from program_review_tool.exceptions import ProgramReviewToolError
from program_review_tool.utils.review.export.config import (
    ASSETS_DIR,
    EXPORT_DIR,
)
from program_review_tool.utils.review.export.mapping_configuration import (
    get_tableau_slide_mapping_df,
)
from program_review_tool.utils.review.export.ppt_generator import (
    populate_title_slide,
    process_tableau_slides,
    remove_multi_pa_slides,
    remove_single_pa_slides,
)
from program_review_tool.utils.review.tableau import (
    sign_in_to_tableau,
    TABLEAU_AUTH_CACHE_TIMEOUT,
    TABLEAU_AUTH_TOKEN_CACHE_KEY_PREFIX,
    TABLEAU_AUTH_TOKEN_EXPIRATION_TEXT,
)


LOGGER = logging.getLogger(__name__)

# Program review complete usage job name.
PROGRAM_REVIEW_COMPLETE_USAGE_JOB_NAME: str = "program_review_complete_usage"

# Presentation template file path.
PPT_TEMPLATE: str = os.path.join(ASSETS_DIR, "PRT.pptx")

PROGRAM_REVIEW_CACHE_PREFIX: str = "program_review_tool_review"

# Default error message used when raising 500 exceptions.
DEFAULT_EXPORT_ERROR_MESSAGE: str = "Failed to generate export."


class ExportStatus:
    """Statuses for the `Program` review PowerPoint export job
    workflow."""

    FAILED = -1
    QUEUED = 0
    IN_PROGRESS = 1
    DONE = 2


@job_decorator("default")
def generate_program_review_powerpoint_wrapper(
    pa_numbers: List[str],
    period: str,
    reviewer_name: str,
    portfolio_name: str,
    export_cache_key: str,
    tableau_token_cache_key: str,
    tableau_token: str,
    generation_id: int,
) -> None:
    """
    Enqueues a job to generate the Program review PowerPoint
    export with the given parameters.

    Accepts:
        * pa_numbers (List[str]): List of pa numbers of `Program`s being reviewed.
        * period (str): Reporting period (i.e. '202501').
        * reviewer_name (str): Name of the `User` that requested the export.
        * portfolio_name (str): Portfolio name.
        * export_cache_key (str): Cache key for the export being generated.
        * tableau_token_cache_key (str): The cache key of the Tableau token used for this
            export job.
        * tableau_token (str): Tableau token used for this export job.
        * generation_id (int): The primary key of the `Usage` instance linked to this job.

    Returns:
        * None
    """

    try:

        export_path: str = generate_program_review_powerpoint(
            pa_numbers=pa_numbers,
            period=period,
            reviewer_name=reviewer_name,
            portfolio_name=portfolio_name,
            export_cache_key=export_cache_key,
            token=tableau_token,
        )

        # Calculate the cache timeout (in seconds) for the export
        # based on the time difference (in seconds) next day at 2:59 AM
        # and the current time.
        current_time = datetime.now()
        expiration_time = (current_time + timedelta(days=1)).replace(
            hour=2, minute=59, second=0, microsecond=0
        )
        cache_timeout = (expiration_time - current_time).total_seconds()
        cache.set(export_cache_key, (ExportStatus.DONE, export_path), cache_timeout)

        # Get the scheduler and queue the job for
        # completing usage.
        scheduler = django_rq.get_scheduler("default")
        scheduler.enqueue_in(
            timedelta(seconds=1),
            controllers.Usage.complete_usage,
            usage_id=generation_id,
            success=True,
            finish_time=timezone.now(),
            meta={
                "job_name": PROGRAM_REVIEW_COMPLETE_USAGE_JOB_NAME,
                "cache_key": export_cache_key,
            },
        )
    except ProgramReviewToolError as exc:
        err_msg = f"Export failed for: {export_cache_key} Reason: {exc.message}"
        LOGGER.error(err_msg)
        cache.set(export_cache_key, (ExportStatus.FAILED, exc.message), 600)

        # Get the scheduler and queue the job for
        # completing usage.
        scheduler = django_rq.get_scheduler("default")
        scheduler.enqueue_in(
            timedelta(seconds=1),
            controllers.Usage.complete_usage,
            usage_id=generation_id,
            success=False,
            error_msg=err_msg,
            finish_time=timezone.now(),
            meta={
                "job_name": PROGRAM_REVIEW_COMPLETE_USAGE_JOB_NAME,
                "cache_key": export_cache_key,
            },
        )

    # Set the Tableau token used for the generation as not `in use`.
    cache.set(
        tableau_token_cache_key, (tableau_token, False), TABLEAU_AUTH_CACHE_TIMEOUT
    )


def generate_program_review_powerpoint(
    pa_numbers: List[str],
    period: str,
    reviewer_name: str,
    portfolio_name: str,
    export_cache_key: str,
    token: str,
) -> str:
    """
    Generates a PowerPoint presentation for the `Program`s and reporting period.

    Accepts:
        * pa_numbers (List[str]): List of pa numbers of `Program`s being reviewed.
        * period (str): Reporting period (i.e. '202501').
        * reviewer_name (str): Name of the `User` that requested the export.
        * portfolio_name (str): Portfolio name.
        * export_cache_key (str): Cache key for the export being generated.
        * token (str): Tableau token used for the retrieval of images.

    Returns:
        * export_path (str): The path to the saved presentation.
    """

    LOGGER.info("Starting presentation generation process.")

    if not pa_numbers:
        raise ProgramReviewToolError("No Programs to review.", 400)
    if not portfolio_name:
        raise ProgramReviewToolError("No Portfolio name given.", 400)

    # Set the export job as `In-Progress` in the cache.
    cache.set(export_cache_key, (ExportStatus.IN_PROGRESS, None))

    # Ensure the template exists.
    if not os.path.exists(PPT_TEMPLATE):
        err_msg = f"Presentation template '{PPT_TEMPLATE}' does not exist."
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(err_msg, 404)

    # Create an export UUID to be used for the subdirectories created
    # for storing the export and the temporary downloaded images
    # from Tableau.
    export_uuid: str = str(uuid.uuid4())
    review_ppt_file_directory_path: str = os.path.join("/tmp/", export_uuid)
    os.mkdir(review_ppt_file_directory_path)

    review_ppt_file_name: str = f"PRT-{portfolio_name}-{period}.pptx"
    review_ppt_file_path: str = os.path.join(
        review_ppt_file_directory_path, review_ppt_file_name
    )
    try:
        # Copy the template to a new file for processing.
        shutil.copyfile(PPT_TEMPLATE, review_ppt_file_path)
        LOGGER.info(
            f"Copied template from '{PPT_TEMPLATE}' to '{review_ppt_file_path}'"
        )
    except Exception as exc:
        err_msg = f"Failed to copy template presentation: {exc}"
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_EXPORT_ERROR_MESSAGE, 500) from exc

    # Load the slide mapping configuration.
    tableau_slide_mapping_df: DataFrame = get_tableau_slide_mapping_df()
    if tableau_slide_mapping_df.empty:
        err_msg = "Tableau slide mapping DataFrame is empty."
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_EXPORT_ERROR_MESSAGE, 500)
    LOGGER.info("Successfully loaded Tableau slide mapping DataFrame.")

    presentation: pptx.Presentation = pptx.Presentation(review_ppt_file_path)
    LOGGER.info(f"Loaded presentation from '{review_ppt_file_path}'.")

    # Populate the title slide.
    try:
        populate_title_slide(presentation, portfolio_name, period, reviewer_name)
        LOGGER.info("Title slide populated successfully.")
    except Exception as exc:
        err_msg = f"Error populating title slide: {exc}"
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_EXPORT_ERROR_MESSAGE, 500) from exc

    # Set `is_multi_pa` flag.
    is_multi_pa: bool = len(pa_numbers) > 1

    # Process and insert Tableau slides.
    try:
        formatted_pa_numbers: str = ",".join(pa_numbers)
        process_tableau_slides(
            presentation,
            tableau_slide_mapping_df,
            period,
            formatted_pa_numbers,
            review_ppt_file_directory_path,
            token,
            is_multi_pa,
        )
        LOGGER.info("Processed Tableau slides successfully.")
    except ProgramReviewToolError as exc:
        raise exc
    except Exception as exc:
        err_msg = f"Error processing Tableau slides: {exc}"
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_EXPORT_ERROR_MESSAGE, 500) from exc

    # For single `Program` reports, remove extra slides.
    if not is_multi_pa:
        remove_multi_pa_slides(presentation, tableau_slide_mapping_df)
    else:
        remove_single_pa_slides(presentation, tableau_slide_mapping_df)

    # Construct the path for the sub-directory, where the presentation
    # will be saved within the export directory, and create it.
    export_file_directory: str = os.path.join(EXPORT_DIR, export_uuid)
    os.mkdir(export_file_directory)

    # Construct the path of the PowerPoint presentation, that will be saved
    # within the `export_file_directory`.
    export_path: str = os.path.join(export_file_directory, review_ppt_file_name)

    # Save the presentation.
    try:
        presentation.save(export_path)
        LOGGER.info(f"Presentation saved to '{export_path}'.")
    except Exception as exc:
        err_msg = f"Error saving presentation: {exc}"
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_EXPORT_ERROR_MESSAGE, 500) from exc

    # Clean up temporary files.
    try:
        temp_files = glob.glob(os.path.join(review_ppt_file_directory_path, "*"))
        shutil.rmtree(review_ppt_file_directory_path)
        LOGGER.info(
            f"Deleted {len(temp_files)} temporary file(s) from '{review_ppt_file_directory_path}'."
        )
    except Exception as exc:
        LOGGER.error(f"Error deleting temporary file(s): {exc}")

    return export_path


def cleanup_expired_exports() -> None:
    """
    Deletes all existing exports in the
    EXPORT_DIR directory path.

    Accepts:
        * None

    Returns:
        * None
    """

    try:
        LOGGER.info("Deleting contents of the export directory...")
        # Delete everything inside EXPORT_DIR directory path including
        # the directory.
        shutil.rmtree(EXPORT_DIR)
        # Re-create the directory in EXPORT_DIR path.
        os.mkdir(EXPORT_DIR)
        LOGGER.info("Successfully deleted the contents of the export directory.")
    except Exception as exc:
        err_msg = f"Failed to cleanup expired exports:{exc}"
        LOGGER.error(err_msg)
