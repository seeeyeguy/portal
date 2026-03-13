"""
`Program Review Tool` `Program` review export utils file
containing common functionality for creating the PowerPoint
export file.
"""

# pylint: disable=wrong-import-order
import logging
import multiprocessing
import os
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from typing import Tuple
from PIL import Image

from django.core.validators import URLValidator

from program_review_tool.exceptions import ProgramReviewToolError
from program_review_tool.utils.review.export.constants import (
    LINK_URL_HEIGHT,
    LINK_URL_LEFT,
    LINK_URL_TOP,
    LINK_URL_WIDTH,
)
from program_review_tool.utils.review.export.pptx_tools import (
    delete_slide,
    find_slide_index_and_slide_by_title,
)

LOGGER = logging.getLogger(__name__)

DEFAULT_POWERPOINT_GENERATION_ERROR: str = "ERROR: Failed to create PowerPoint."

# Configuration for concurrent PowerBI exports
MAX_TOTAL_WAIT_TIME = 300  # 5 minutes maximum for all exports
POLL_CYCLE_INTERVAL = 3  # Checkall exports every 3 seconds


def populate_title_slide(
    presentation: Presentation,  # type: ignore[valid-type]
    title_slide_name: str,
    period: str,
    program_manager_names: str,
) -> None:
    """
    Populates the title slide with `Program` data and provided parameters.

    Accepts:
        * presentation (Presentation): The presentation to modify.
        * title_slide_name (str): Name of the title slide of the
            presentation.
        * period (str): Reporting period.
        * program_manager_names (str): Names of the `Program` manager(s).

    Returns:
        * None
    """

    # Populate the first slide (assumed title slide).
    slide = presentation.slides[0]  # type: ignore[attr-defined]
    try:
        slide.placeholders[0].text = title_slide_name
        slide.placeholders[1].text = format_period(period)
        slide.placeholders[10].text = datetime.now().strftime("%B %-d, %Y")
        LOGGER.info(f"program manager: {program_manager_names}")
        slide.placeholders[11].text = f"{program_manager_names}"

        # Unbold the program manager names if needed
        for paragraph in slide.placeholders[11].text_frame.paragraphs:
            for run in paragraph.runs:
                run.font.bold = False

    except Exception as exc:
        err_msg = f"Error populating title slide placeholders: {exc}"
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_POWERPOINT_GENERATION_ERROR, 500) from exc


def write_image_to_slide(
    presentation: Presentation,  # type: ignore[valid-type]
    image_path: str,
    title_name: str,
    height: float,
    width: float,
    top: float,
    left: float,
    link_url: str,
) -> bool:
    """
    Inserts an image into a slide with an optional hyperlink.

    Accepts:
        * presentation (Presentation): The presentation object.
        * image_path (str): Path to the image file.
        * title_name (str): The title of the target slide.
        * height (float): Image height in inches.
        * width (float): Image width in inches.
        * top (float): Top margin in inches.
        * left (float): Left margin in inches.
        * link_url (str): Hyperlink for the image (if applicable).

    Returns:
        * bool: True if the image is inserted successfully; False otherwise.
    """

    if not os.path.exists(image_path):
        LOGGER.error(f"Image file '{image_path}' does not exist.")
        return False

    slide_pair = find_slide_index_and_slide_by_title(presentation, title_name)
    if not slide_pair:
        return False

    _, slide = slide_pair

    try:
        sp_tree = slide.shapes._spTree
        # Insert the image.
        slide.shapes.add_picture(
            image_path, Inches(left), Inches(top), Inches(width), Inches(height)
        )
        # Reorder shapes to preserve layering.
        all_shapes = list(slide.shapes)
        for shape in all_shapes:
            sp_tree.remove(shape._element)
        for shape in reversed(all_shapes):
            sp_tree.insert(len(sp_tree), shape._element)

        # If a valid link is provided, add a hyperlink textbox.
        # TODO: currently this validator just throws an exception
        #       but we should better handle this in the future
        validate = URLValidator()
        validate(link_url)
        
        if len(link_url):            
            textbox = slide.shapes.add_textbox(
                Inches(LINK_URL_LEFT),
                Inches(LINK_URL_TOP),
                Inches(LINK_URL_WIDTH),
                Inches(LINK_URL_HEIGHT),
            )
            text_frame = textbox.text_frame
            paragraph = text_frame.paragraphs[0]
            paragraph.alignment = PP_ALIGN.RIGHT
            run = paragraph.add_run()
            run.text = "Link to Dashboard"
            run.font.underline = True
            run.font.color.rgb = RGBColor(0, 0, 255)
            run.font.size = Pt(14)
            run.font.name = "Arial"
            run.hyperlink.address = link_url

        return True
    except Exception as exc:
        LOGGER.error(
            f"Error inserting image '{image_path}' into slide '{title_name}': {exc}"
        )
        return False

def process_powerbi_slides(
    presentation: Presentation,  # type: ignore[valid-type]
    slides_config: list,
    project_ids: list,
    images_directory: str,
    token: str,
    is_multi_pa: bool,
) -> None:
    """
    Processes PowerBI slides by initiating all exports concurrently, then polling
    and downloading as they complete.

    This concurrent implementation is much faster than serial processing:
    - Phase 1: Initiate all exports (PowerBI processes in parallel)
    - Phase 2: Poll all exports concurrently (non-blocking)
    - Phase 3: Download and insert images as they complete

    Accepts:
        * presentation (Presentation): The presentation object.
        * slides_config (list): List of slide configuration dictionaries from JSON.
        * project_ids (list): List of project IDs to include in the export.
        * images_directory (str): Directory for saving images.
        * token (str): PowerBI authentication token.
        * is_multi_pa (bool): Flag for multi-project context.

    Returns:
        * None
    """
    from program_review_tool.utils.review.powerbi.powerbi_export import (
        initiate_export,
        build_export_request_body,
        check_export_status,
        retrieve_export_file,
    )

    LOGGER.info(
        f"Processing {len(slides_config)} PowerBI slides for "
            f"{'multi' if is_multi_pa else 'single'}-PA report (CONCURRENT MODE)"
    )

    # Filter slides based on pa_type
    filtered_slides = []
    for slide in slides_config:
        pa_type = slide.get('pa_type', 'both')

        if pa_type == 'both':
            filtered_slides.append(slide)
        elif pa_type == 'omit':
            continue 
        elif pa_type == 'single' and not is_multi_pa:
            filtered_slides.append(slide)
        elif pa_type == 'multi' and is_multi_pa:
            filtered_slides.append(slide)

    LOGGER.info(f"After filtering by pa_type: {len(filtered_slides)} slides to process")

    if not filtered_slides:
        LOGGER.info("No slides to process")
        return

    # ========================================================================
    # PHASE 1: INITIATE ALL EXPORTS (Fast - just submit requests)
    # ========================================================================
    LOGGER.info("=" * 80)
    LOGGER.info("PHASE 1: Initiating all exports concurrently...")
    LOGGER.info("=" * 80)

    export_jobs = []
    failed_initiations = []

    for slide_config in filtered_slides:
        slide_title = slide_config.get('slide_title')
        workspace_id = slide_config.get('workspace_id')
        report_id = slide_config.get('report_id')
        page_name = slide_config.get('pageName')

        try:
            LOGGER.info(f"  Initiating export for: {slide_title}")

            # Extract project filter details
            project_filter = slide_config.get('project_filter', {})
            project_filter_table = project_filter.get('table_name')
            project_filter_column = project_filter.get('column_name')

            # Build request body
            request_body = build_export_request_body(
                page_name=page_name,
                project_ids=project_ids,
                project_filter_table=project_filter_table or "",
                project_filter_column=project_filter_column or "",
                identity=slide_config.get('identity')
            )

            # Initiate export (non-blocking - just get export ID)
            export_id = initiate_export(
                workspace_id=workspace_id,
                report_id=report_id,
                request_body=request_body,
                token=token
            )

            # Create output path
            slide_num = slide_config.get('slide_num', 'unknown')
            output_filename = f"slide_{slide_num}_{workspace_id}_{page_name}.png"
            output_path = os.path.join(images_directory, output_filename)

            # Store job info for polling
            export_jobs.append({
                'slide_title': slide_title,
                'slide_config': slide_config,
                'workspace_id': workspace_id,
                'report_id': report_id,
                'export_id': export_id,
                'output_path': output_path,
                'status': 'Pending',
                'initiated_at': time.time(),
            })

            LOGGER.info(f"  ✓ Export initiated: {slide_title} (Export ID: {export_id[:30]}...)")

        except Exception as exc:
            LOGGER.error(f"  ✗ Failed to initiate export for '{slide_title}': {exc}")
            failed_initiations.append(slide_title)
            continue

    LOGGER.info(
        f"PHASE 1 Complete: {len(export_jobs)} exports initiated, "
            f"{len(failed_initiations)} failed"
    )

    if not export_jobs:
        LOGGER.error("No exports were successfully initiated. Aborting.")
        return

    # ========================================================================
    # PHASE 2: POLL ALL EXPORTS CONCURRENTLY
    # TODO: Extend polling interval to 5s; once ane export is finished, have 
    #       it start the download process between polling intervals
    # ========================================================================
    LOGGER.info("=" * 80)
    LOGGER.info("PHASE 2: Polling exports concurrently...")
    LOGGER.info("=" * 80)

    pending_jobs = export_jobs.copy()
    completed_jobs = []
    failed_jobs = []

    start_time = time.time()
    poll_cycle = 0

    while pending_jobs:
        poll_cycle += 1
        elapsed = time.time() - start_time

        # Check timeout
        if elapsed > MAX_TOTAL_WAIT_TIME:
            LOGGER.error(
                f"Timeout after {MAX_TOTAL_WAIT_TIME}s. "
                    f"{len(pending_jobs)} exports still pending."
            )
            failed_jobs.extend(pending_jobs)
            break

        LOGGER.info(
            f"Poll cycle {poll_cycle}: Checking {len(pending_jobs)} pending exports "
                f"(elapsed: {int(elapsed)}s)"
        )

        # Check status of all pending jobs
        jobs_to_remove = []

        for job in pending_jobs:
            try:
                # Quick status check (non-blocking)
                status = check_export_status(
                    workspace_id=job['workspace_id'],
                    report_id=job['report_id'],
                    export_id=job['export_id'],
                    token=token
                )

                if status == 'Succeeded':
                    LOGGER.info(f"  ✓ {job['slide_title']}: Succeeded")
                    job['status'] = 'Succeeded'
                    completed_jobs.append(job)
                    jobs_to_remove.append(job)

                elif status == 'Failed':
                    LOGGER.error(f"  ✗ {job['slide_title']}: Failed")
                    job['status'] = 'Failed'
                    failed_jobs.append(job)
                    jobs_to_remove.append(job)

                elif status == 'Running':
                    job_elapsed = time.time() - job['initiated_at']
                    LOGGER.debug(
                        f"  ⏳ {job['slide_title']}: Still running ({int(job_elapsed)}s)"
                    )

                else:
                    LOGGER.warning(f"  ? {job['slide_title']}: Unknown status: {status}")

            except Exception as exc:
                LOGGER.error(f"  ✗ {job['slide_title']}: Error checking status: {exc}")
                job['status'] = 'Error'
                job['error'] = str(exc)
                failed_jobs.append(job)
                jobs_to_remove.append(job)

        # Remove completed/failed jobs from pending list
        for job in jobs_to_remove:
            pending_jobs.remove(job)

        # If there are still pending jobs, wait before next poll cycle
        if pending_jobs:
            LOGGER.info(
                f"  Waiting {POLL_CYCLE_INTERVAL}s before next poll cycle... "
                    f"({len(completed_jobs)} done, {len(pending_jobs)} pending, "
                    f"{len(failed_jobs)} failed)"
            )
            time.sleep(POLL_CYCLE_INTERVAL)

    LOGGER.info(
        f"PHASE 2 Complete: {len(completed_jobs)} succeeded, "
            f"{len(failed_jobs)} failed, total time: {int(time.time() - start_time)}s"
    )

    # ========================================================================
    # PHASE 3: DOWNLOAD AND INSERT COMPLETED EXPORTS
    # ========================================================================
    LOGGER.info("=" * 80)
    LOGGER.info("PHASE 3: Downloading and inserting images...")
    LOGGER.info("=" * 80)

    inserted_count = 0

    for job in completed_jobs:
        slide_title = job['slide_title']
        slide_config = job['slide_config']

        try:
            LOGGER.info(f"  Processing: {slide_title}")

            # Download the export file
            image_path = retrieve_export_file(
                workspace_id=job['workspace_id'],
                report_id=job['report_id'],
                export_id=job['export_id'],
                output_path=job['output_path'],
                token=token
            )

            if not image_path or not os.path.exists(image_path):
                LOGGER.error(f"  ✗ Image file not found: {image_path}")
                continue

            # Insert the image into the slide
            image_container_size = slide_config.get('image_container_size', {})
            layout = slide_config.get('layout', {})
            link_url = slide_config.get('link_url', '')

            # Check if the image should be cropped
            crop_config = slide_config.get('crop')

            if crop_config:
                img = Image.open(image_path)
                #LOGGER.info(f"Cropping image: {image_path} using crop config: {crop_config}")
                img = img.crop((crop_config['left'], crop_config['top'], crop_config['right'], crop_config['bottom']))
                img.save(image_path)

            success = write_image_to_slide(
                presentation,
                image_path,
                slide_title,
                height=image_container_size.get('height', 4.93),
                width=image_container_size.get('width', 9.61),
                top=layout.get('top', 1.2),
                left=layout.get('left', 0.2),
                link_url=link_url,
            )

            if success:
                LOGGER.info(f"  ✓ Successfully inserted: {slide_title}")
                inserted_count += 1
            else:
                LOGGER.error(f"  ✗ Failed to insert: {slide_title}")

        except Exception as exc:
            LOGGER.error(f"  ✗ Error processing '{slide_title}': {exc}")
            import traceback
            traceback.print_exc()
            continue

    LOGGER.info(
        f"PHASE 3 Complete: {inserted_count}/{len(completed_jobs)} images inserted"
    )

    # ========================================================================
    # SUMMARY
    # ========================================================================
    LOGGER.info("=" * 80)
    LOGGER.info("POWERBI EXPORT SUMMARY (CONCURRENT MODE)")
    LOGGER.info("=" * 80)
    LOGGER.info(f"Total slides requested: {len(filtered_slides)}")
    LOGGER.info(f"Exports initiated: {len(export_jobs)}")
    LOGGER.info(f"Exports succeeded: {len(completed_jobs)}")
    LOGGER.info(f"Exports failed: {len(failed_jobs)}")
    LOGGER.info(f"Images inserted: {inserted_count}")
    LOGGER.info(f"Total time: {int(time.time() - start_time)}s")
    LOGGER.info("=" * 80)

    if failed_jobs:
        LOGGER.warning("Failed slides:")
        for job in failed_jobs:
            error_msg = job.get('error', 'Export failed or timed out')
            LOGGER.warning(f"  - {job['slide_title']}: {error_msg}")


def remove_multi_pa_slides(
    presentation: Presentation,  # type: ignore[valid-type]
    slides_config: list,
) -> None:
    """
    Removes slides that are not applicable for single PA reports.

    When generating a SINGLE PA report:
    - Keep slides with pa_type = "single" or "both"
    - Remove slides with pa_type = "multi" or "omit"

    Accepts:
        * presentation (pptx.Presentation): The presentation object.
        * slides_config (list): List of slide configuration dictionaries from JSON.

    Returns:
        * None
    """

    # Collect slides to delete first (don't delete while iterating)
    slides_to_delete = []

    for slide_config in slides_config:
        pa_type = slide_config.get('pa_type', 'both')

        LOGGER.info(f"Slide {slide_config['slide_title']} pa_type: {pa_type}")
        # If pa_type is "multi" or "omit", this slide should NOT be in single-PA reports
        if pa_type in ('multi', 'omit'):
            slide_title = slide_config['slide_title']
            slide_pair = find_slide_index_and_slide_by_title(presentation, slide_title)

            if slide_pair is not None:
                slide_index, _ = slide_pair
                slides_to_delete.append((slide_index, slide_title))
            else:
                LOGGER.warning(
                    f"Slide to delete with title '{slide_title}' was not found."
                )

    # Sort by index in descending order and delete from the end
    # This prevents index shifting issues
    slides_to_delete.sort(key=lambda x: x[0], reverse=True)

    for slide_index, slide_title in slides_to_delete:
        # Adjust slide index to 0-based index when deleting
        delete_slide(presentation, slide_index - 1)
        LOGGER.info(f"Deleted multi-PA/omit slide: {slide_title} (index {slide_index})")


def remove_single_pa_slides(
    presentation: Presentation,  # type: ignore[valid-type]
    slides_config: list,
) -> None:
    """
    Removes slides that are not applicable for multi-PA reports.

    When generating a MULTI-PA report:
    - Keep slides with pa_type = "multi" or "both"
    - Remove slides with pa_type = "single" or "omit"

    Accepts:
        * presentation (pptx.Presentation): The presentation object.
        * slides_config (list): List of slide configuration dictionaries from JSON.

    Returns:
        * None
    """

    # Collect slides to delete first (don't delete while iterating)
    slides_to_delete = []

    for slide_config in slides_config:
        pa_type = slide_config.get('pa_type', 'both')

        LOGGER.info(f"Slide {slide_config['slide_title']} pa_type: {pa_type}")

        # If pa_type is "single" or "omit", this slide should NOT be in multi-PA reports
        if pa_type in ('single', 'omit'):
            slide_title = slide_config['slide_title']
            slide_pair = find_slide_index_and_slide_by_title(presentation, slide_title)

            if slide_pair is not None:
                slide_index, _ = slide_pair
                slides_to_delete.append((slide_index, slide_title))
            else:
                LOGGER.warning(
                    f"Slide to delete with title '{slide_title}' was not found."
                )

    # Sort by index in descending order and delete from the end
    # This prevents index shifting issues
    slides_to_delete.sort(key=lambda x: x[0], reverse=True)

    for slide_index, slide_title in slides_to_delete:
        # Adjust slide index to 0-based index when deleting
        delete_slide(presentation, slide_index - 1)
        LOGGER.info(f"Deleted single-PA/omit slide: {slide_title} (index {slide_index})")


def format_period(yyyymm: str) -> str:
    """Convert a YYYYMM string into YYYY-PMM format."""
    year = yyyymm[:4]
    month = yyyymm[4:]
    return f"{year}-P{month}"
