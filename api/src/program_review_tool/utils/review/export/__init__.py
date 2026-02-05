"""
`Program Review Tool` `Program` review export utils module.
Common functionality for `Program Review Tool` `Program` app
to help with generating the `Program` review PowerPoint export.

Updated to use PowerBI API instead of Tableau.
"""

# pylint: disable=wrong-import-order
import glob
import logging
import os
import pptx
import re
import shutil
import uuid
from datetime import datetime, timedelta
from typing import List

import django_rq
from django.core.cache import cache
from django_rq import job as job_decorator
from django.utils import timezone

from manager.settings import PROGRAM_REVIEW_EXPORT_CACHE_TIMEOUT_SECONDS
from program_review_tool.exceptions import ProgramReviewToolError
from program_review_tool.utils.review.export.config import (
    ASSETS_DIR,
    EXPORT_DIR,
)
from program_review_tool.utils.review.export.mapping_configuration import (
    load_slides_config,
    get_powerbi_slide_mapping_df,
)
from program_review_tool.utils.review.export.ppt_generator import (
    populate_title_slide,
    process_powerbi_slides,
    remove_multi_pa_slides,
    remove_single_pa_slides,
)
from program_review_tool.utils.review.powerbi.config import (
    AZURE_TOKEN_CACHE_KEY,
)

LOGGER = logging.getLogger(__name__)

# Program review complete usage job name.
PROGRAM_REVIEW_COMPLETE_USAGE_JOB_NAME: str = "program_review_complete_usage"

# Presentation template file path.
PPT_TEMPLATE: str = os.path.join(ASSETS_DIR, "PRT.pptx")

PROGRAM_REVIEW_CACHE_PREFIX: str = "program_review_tool_review"

# Default error message used when raising 500 exceptions.
DEFAULT_EXPORT_ERROR_MESSAGE: str = "Failed to generate export."

# Azure AD token cache timeout (1 hour minus 10% for safety)
AZURE_AUTH_CACHE_TIMEOUT:int = int(os.getenv("AZURE_AUTH_CACHE_TIMEOUT", 3240))

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
    program_manager_names: str,
    review_name: str,
    export_cache_key: str,
    powerbi_token_cache_key: str,
    powerbi_token: str,
    usage_id: int,
) -> None:
    """
    Enqueues a job to generate the Program review PowerPoint
    export with the given parameters.

    Accepts:
        * pa_numbers (List[str]): List of pa numbers of `Program`s being reviewed.
        * period (str): Reporting period (i.e. '202501').
        * program_manager_names (str): Names of the `Program` manager(s).
        * review_name (str): Review name.
        * export_cache_key (str): Cache key for the export being generated.
        * powerbi_token_cache_key (str): The cache key of the PowerBI token used for this
            export job.
        * powerbi_token (str): Azure AD access token used for this export job.
        * usage_id (int): The primary key of the `Usage` instance linked to this job.

    Returns:
        * None
    """

    # LAZY IMPORT: Import controllers here to avoid circular dependency
    from program_review_tool import controllers

    try:

        export_path: str = generate_program_review_powerpoint(
            pa_numbers=pa_numbers,
            period=period,
            program_manager_names=program_manager_names,
            portfolio_name=review_name,
            export_cache_key=export_cache_key,
            token=powerbi_token,
        )

        cache_timeout = PROGRAM_REVIEW_EXPORT_CACHE_TIMEOUT_SECONDS
        cache.set(export_cache_key, (ExportStatus.DONE, export_path), cache_timeout)

        # Get the scheduler and queue the job for
        # completing usage.
        scheduler = django_rq.get_scheduler("default")
        scheduler.enqueue_in(
            timedelta(seconds=1),
            controllers.Usage.complete_usage,
            usage_id=usage_id,
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
            usage_id=usage_id,
            success=False,
            error_msg=err_msg,
            finish_time=timezone.now(),
            meta={
                "job_name": PROGRAM_REVIEW_COMPLETE_USAGE_JOB_NAME,
                "cache_key": export_cache_key,
            },
        )

    # Set the PowerBI token used for the generation as not `in use`.
    cache.set(
        powerbi_token_cache_key, (powerbi_token, False), AZURE_AUTH_CACHE_TIMEOUT
    )


def generate_program_review_powerpoint(
    pa_numbers: List[str],
    period: str,
    program_manager_names: str,
    portfolio_name: str,
    export_cache_key: str,
    token: str,
) -> str:
    """
    Generates a PowerPoint presentation for the `Program`s and reporting period.

    Accepts:
        * pa_numbers (List[str]): List of pa numbers of `Program`s being reviewed.
        * period (str): Reporting period (i.e. '202501').
        * program_manager_names (str): Names of the `Program` manager(s).
        * portfolio_name (str): Portfolio name.
        * export_cache_key (str): Cache key for the export being generated.
        * token (str): Azure AD access token used for PowerBI API calls.

    Returns:
        * export_path (str): The path to the saved presentation.
    """

    def generate_ppt_filename(portfolio_name: str, period: str) -> str:
        """
        Generates the filename of the PowerPoint export, using
        the given Portfolio name and period.
        Accepts:
            * portfolio_name (str): Portfolio name.
            * period (str): Reporting period (i.e. '202501').
        Returns:
            * ppt_filename (str): Filename of the PowerPoint export.
        """

        # Cleanup any unwanted special characters from Portfolio name.
        cleaned_portfolio_name: str = re.sub(
            r'[\\/:*?@`!#(){},;^~"<>|]', "_", portfolio_name
        )
        # Replace any continous underscores, in the `cleaned_portfolia_name`,
        # with a single one.
        cleaned_portfolio_name = re.sub(r"__+", "_", cleaned_portfolio_name)

        cleaned_portfolio_name = cleaned_portfolio_name.strip()

        ppt_filename: str = f"PRT-{cleaned_portfolio_name}-{period}.pptx"

        return ppt_filename

    LOGGER.info("Starting presentation generation process.")

    if not pa_numbers:
        raise ProgramReviewToolError("No Programs to review.", 400)
    if not portfolio_name:
        raise ProgramReviewToolError("No Portfolio name given.", 400)

    # If the EXPORT_DIR does not exist, attempt to re-create it.
    try:
        if not os.path.exists(EXPORT_DIR):
            os.mkdir(EXPORT_DIR)
    except Exception as exc:
        err_msg = f"Failed to create missing EXPORT_DIR: {EXPORT_DIR} due to: {exc}"
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_EXPORT_ERROR_MESSAGE, 500) from exc

    # Set the export job as `In-Progress` in the cache.
    cache.set(export_cache_key, (ExportStatus.IN_PROGRESS, None))

    # Ensure the template exists.
    if not os.path.exists(PPT_TEMPLATE):
        err_msg = f"Presentation template '{PPT_TEMPLATE}' does not exist."
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(err_msg, 404)

    # Create an export UUID to be used for the subdirectories created
    # for storing the export and the temporary downloaded images
    # from PowerBI.
    export_uuid: str = str(uuid.uuid4())
    review_ppt_file_directory_path: str = os.path.join("/tmp/", export_uuid)
    os.mkdir(review_ppt_file_directory_path)

    review_ppt_file_name: str = generate_ppt_filename(portfolio_name, period)
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

    # Load the slide configuration.
    try:
        slides_config = load_slides_config(validate_schema=True)
        slides = slides_config.get('slides', [])

        if not slides:
            err_msg = "Slides configuration is empty."
            LOGGER.error(err_msg)
            raise ProgramReviewToolError(DEFAULT_EXPORT_ERROR_MESSAGE, 500)

        LOGGER.info(f"Successfully loaded {len(slides)} slides from configuration.")
    except Exception as exc:
        err_msg = f"Failed to load slides configuration: {exc}"
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_EXPORT_ERROR_MESSAGE, 500) from exc

    presentation: pptx.Presentation = pptx.Presentation(review_ppt_file_path)  # type: ignore[unused-ignore,valid-type]
    LOGGER.info(f"Loaded presentation from '{review_ppt_file_path}'.")

    # Populate the title slide.
    try:
        populate_title_slide(
            presentation, portfolio_name, period, program_manager_names
        )
        LOGGER.info("Title slide populated successfully.")
    except Exception as exc:
        err_msg = f"Error populating title slide: {exc}"
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_EXPORT_ERROR_MESSAGE, 500) from exc

    # Set `is_multi_pa` flag.
    is_multi_pa: bool = len(pa_numbers) > 1

    # Process and insert PowerBI slides.
    try:
        process_powerbi_slides(
            presentation=presentation,
            slides_config=slides,
            project_ids=pa_numbers,  # Now expects a list, not comma-separated string
            images_directory=review_ppt_file_directory_path,
            token=token,
            is_multi_pa=is_multi_pa,
        )
        LOGGER.info("Processed PowerBI slides successfully.")
    except ProgramReviewToolError as exc:
        raise exc
    except Exception as exc:
        err_msg = f"Error processing PowerBI slides: {exc}"
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_EXPORT_ERROR_MESSAGE, 500) from exc

    # For single `Program` reports, remove extra slides.
    if not is_multi_pa:
        remove_multi_pa_slides(presentation, slides)
    else:
        remove_single_pa_slides(presentation, slides)

    # Construct the path for the sub-directory, where the presentation
    # will be saved within the export directory, and create it.
    export_file_directory: str = os.path.join(EXPORT_DIR, export_uuid)
    os.mkdir(export_file_directory)

    LOGGER.info(f"Export path: {export_file_directory}")
    # Construct the path of the PowerPoint presentation, that will be saved
    # within the `export_file_directory`.
    export_path: str = os.path.join(export_file_directory, review_ppt_file_name)

    # Save the presentation.
    try:
        presentation.save(export_path)  # type: ignore[unused-ignore,attr-defined]
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

        # Get list of items in EXPORT_DIR.
        export_dir_items = os.listdir(EXPORT_DIR)

        # Loop through each item, construct its path
        # and, if the item is a directory, delete it.
        for item in export_dir_items:
            item_path = os.path.join(EXPORT_DIR, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)

        LOGGER.info("Successfully deleted the contents of the export directory.")
    except Exception as exc:
        err_msg = f"Failed to cleanup expired exports:{exc}"
        LOGGER.error(err_msg)
