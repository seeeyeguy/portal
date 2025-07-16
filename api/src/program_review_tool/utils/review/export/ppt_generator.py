"""
`Program Review Tool` `Program` review export utils file
containing common functionality for creating the PowerPoint
export file.
"""

# pylint: disable=wrong-import-order
import logging
import os
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.slide import Slide
from pptx.util import Inches, Pt
from typing import Optional, Tuple

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
from program_review_tool.utils.review.tableau import get_and_save_view_image
from program_review_tool.utils.review.tableau.config import (
    TABLEAU_API_VERSION,
    TABLEAU_SERVER,
)


LOGGER = logging.getLogger(__name__)

TABLEAU_VIEW_BASE_URI: str = f"{TABLEAU_SERVER}/api/{TABLEAU_API_VERSION}/sites/795095c9-90ab-470c-b6c6-a14e92993b5b/views/"

DEFAULT_POWERPOINT_GENERATION_ERROR: str = "ERROR: Failed to create PowerPoint."


def populate_title_slide(
    presentation: Presentation,
    title_slide_name: str,
    period: str,
    reviewer_name: str,
) -> None:
    """
    Populates the title slide with `Program` data and provided parameters.

    Accepts:
        * presentation (Presentation): The presentation to modify.
        * title_slide_name (str): Name of the title slide of the
            presentation.
        * period (str): Reporting period.
        * reviewer_name (str): Name of the `User` that requested the export.

    Returns:
        * None
    """

    # Populate the first slide (assumed title slide).
    slide = presentation.slides[0]
    try:
        slide.placeholders[0].text = title_slide_name
        slide.placeholders[1].text = format_period(period)
        slide.placeholders[10].text = datetime.now().strftime("%B, %-d %Y")
        slide.placeholders[11].text = "Program Manager: "
    except Exception as exc:
        err_msg = f"Error populating title slide placeholders: {exc}"
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_POWERPOINT_GENERATION_ERROR, 500) from exc


def write_tableau_image_to_slide(
    presentation: Presentation,
    image_path: str,
    title_name: str,
    height: float,
    width: float,
    top: float,
    left: float,
    link_url: str,
) -> bool:
    """
    Inserts a Tableau generated image into a slide with an optional hyperlink.

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
        validate = URLValidator()
        validate(link_url)
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


def download_image(
    row: pd.Series,
    tableau_view_base_uri: str,
    period: str,
    pa_numbers: str,
    images_directory: str,
    token: str,
) -> Tuple[str, str]:
    """
    Downloads an image from Tableau based on configuration settings in the row.

    Accepts:
        * row (pd.Series): Row with slide configuration.
        * tableau_view_base_uri (str): Base URL for Tableau views.
        * period (str): Reporting period.
        * pa_numbers (str): Comma-separated pa numbers used for fetching
            images from Tableau (i.e.'11LN,12RV').
        * images_directory (str): Directory to save images.
        * token (str): Tableau authentication token.

    Returns:
        * Tuple[str, str]: A tuple with the slide title and image file name (without extension).
    """

    start_time = time.perf_counter()

    try:
        date_str = str(row.date_format)
        period_param = period[:4] if len(date_str) == 4 else period
        uri = (
            f"{tableau_view_base_uri.strip()}{str(row.internal_view_id).strip()}/image"
            f"?vf_{str(row.pa_code_filter).strip()}={pa_numbers}&maxAge=1&vf_None={period_param}"
        )
        file_name = f"{row.internal_view_id}"
        image_path_name = os.path.join(images_directory, f"{file_name}.png")
        get_and_save_view_image(uri, image_path_name, token)
        LOGGER.debug(
            f"Downloaded image for slide '{row.slide_title}', saved as '{image_path_name}'."
        )
        elapsed = time.perf_counter() - start_time
        LOGGER.debug(f"Fetching {uri} took {elapsed:.2f} seconds")
        return row.slide_title, file_name
    except Exception as exc:
        err_msg = f"Error downloading image: {exc}"
        LOGGER.error(err_msg)
        raise ProgramReviewToolError(DEFAULT_POWERPOINT_GENERATION_ERROR, 500) from exc


def process_tableau_slides(
    presentation: Presentation,
    tableau_slide_mapping_df: pd.DataFrame,
    period: str,
    pa_numbers: str,
    images_directory: str,
    token: str,
    is_multi_pa: bool,
) -> None:
    """
    Processes Tableau slides by downloading images concurrently and inserting them into
    the presentation.

    Accepts:
        * presentation (Presentation): The presentation object.
        * tableau_slide_mapping_df (pd.DataFrame): DataFrame with slide mapping settings.
        * period (str): Reporting period.
        * pa_numbers (str): Comma-separated pa numbers used for fetching
            images from Tableau (i.e.'11LN,12RV').
        * images_directory (str): Directory for saving images.
        * token (str): Tableau authentication token.
        * is_multi_pa (bool): Flag for multi-project context.

    Returns:
        * None
    """

    file_to_slide_mapping = []

    rows = (
        tableau_slide_mapping_df.itertuples()
        if is_multi_pa
        else tableau_slide_mapping_df[
            tableau_slide_mapping_df["isSinglePa"]
        ].itertuples()
    )
    with ThreadPoolExecutor(max_workers=16) as executor:
        future_to_row = {
            executor.submit(
                download_image,
                row,
                TABLEAU_VIEW_BASE_URI,
                period,
                pa_numbers,
                images_directory,
                token,
            ): row
            for row in rows
        }
        for future in as_completed(future_to_row):
            row = future_to_row[future]
            try:
                slide_title, file_name = future.result()
                file_to_slide_mapping.append(
                    {
                        "slide_title": slide_title,
                        "file_name": file_name,
                        "height": row.height,
                        "width": row.width,
                        "top": row.top,
                        "left": row.left,
                        "linkUrl": row.linkUrl,
                    }
                )
            except Exception as exc:
                LOGGER.error(f"Error processing row {row}: {exc}")

    # Insert images into slides.
    for slide_data in file_to_slide_mapping:
        image_path = os.path.join(images_directory, f"{slide_data['file_name']}.png")
        if not os.path.exists(image_path):
            LOGGER.error(
                f"Image file '{image_path}' not found. Skipping slide '{slide_data['slide_title']}'."
            )
            continue
        success = write_tableau_image_to_slide(
            presentation,
            image_path,
            slide_data["slide_title"],
            slide_data["height"],
            slide_data["width"],
            slide_data["top"],
            slide_data["left"],
            slide_data["linkUrl"],
        )
        if not success:
            LOGGER.error(
                f"Failed to insert image '{image_path}' into slide '{slide_data['slide_title']}'."
            )


def remove_multi_pa_slides(
    presentation: Presentation,
    tableau_slide_mapping_df: pd.DataFrame,
) -> None:
    """
    Removes slides that are not applicable for single PA reports.

    Accepts:
        * presentation (pptx.Presentation): The presentation object.
        * tableau_slide_mapping_df (pd.DataFrame): Mapping DataFrame indicating slide applicability.

    Returns:
        * None
    """

    for row in tableau_slide_mapping_df[
        ~tableau_slide_mapping_df["isSinglePa"]
    ].itertuples():
        slide_pair = find_slide_index_and_slide_by_title(presentation, row.slide_title)
        if slide_pair is not None:
            slide_index, _ = slide_pair
            # Adjust slide index to 0-based index when deleting.
            delete_slide(presentation, slide_index - 1)
            LOGGER.info(f"Deleted slide number: {slide_index}")
        else:
            LOGGER.warning(
                f"Slide to delete with title '{row.slide_title}' was not found."
            )

def remove_single_pa_slides(
    presentation: Presentation,
    tableau_slide_mapping_df: pd.DataFrame,
) -> None:
    """
    Removes slides that are not applicable for multi-PA reports.

    Accepts:
        * presentation (pptx.Presentation): The presentation object.
        * tableau_slide_mapping_df (pd.DataFrame): Mapping DataFrame indicating slide applicability.

    Returns:
        * None
    """

    for row in tableau_slide_mapping_df[
        ~tableau_slide_mapping_df["isMultiPa"]
    ].itertuples():
        slide_pair = find_slide_index_and_slide_by_title(presentation, row.slide_title)
        if slide_pair is not None:
            slide_index, _ = slide_pair
            # Adjust slide index to 0-based index when deleting.
            delete_slide(presentation, slide_index - 1)
            LOGGER.info(f"Deleted slide number: {slide_index}")
        else:
            LOGGER.warning(
                f"Slide to delete with title '{row.slide_title}' was not found."
            )
            
def format_period(yyyymm: str) -> str:
    """Convert a YYYYMM string into YYYY-PMM format."""
    year = yyyymm[:4]
    month = yyyymm[4:]
    return f"{year}-P{month}"