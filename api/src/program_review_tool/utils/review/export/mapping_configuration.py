"""
`Program Review Tool` `Program` review export utils file
containing common functionality for getting the
Tableau slide mapping used in the generation
of the PowerPoint export.
"""

import os
import pandas as pd

from program_review_tool.utils.review.export.config import ASSETS_DIR


SLIDES_CSV_PATH: str = os.path.join(ASSETS_DIR, "slides.csv")


def get_tableau_slide_mapping_df() -> pd.DataFrame:
    """
    Loads the Tableau slide mapping configuration from a CSV file.

    Accepts:
        * None

    Returns:
        * mapping_df (pd.DataFrame): DataFrame containing slide mapping configuration.
    """

    mapping_df: pd.DataFrame = (
        pd.read_csv(SLIDES_CSV_PATH)
        if os.path.exists(SLIDES_CSV_PATH)
        else pd.DataFrame()
    )

    return mapping_df
