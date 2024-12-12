"""
Parser script module. Module provide parser that
may read a .csv/.xls/.xlsx file, and return a
DataFrame if and only if, that file is devoid
of errors, else reject that file.   
"""

from typing import Callable, List
import pandas as pd


class Parser:
    """
    Container class for functionality related to parsing
    a file (.csv/.xls/.xlsx) and generating a DataFrame
    that we may use to generate a fixture dataset.
    """

    @staticmethod
    def read_file(path: str, sheet: str) -> pd.DataFrame:
        """Read a .csv/.xls/.xlsx file and return a DataFrame."""

        converters = {
            key: str.strip
            for key in (
                "Function",
                "SubFunction",
                "Site",
                "Display Name",
                "Description",
                "Tags",
                "Restricted",
            )
        }

        try:
            df = pd.read_excel(path, sheet_name=sheet, converters=converters)
        except (ValueError, FileNotFoundError):
            df = pd.read_csv(path, header=0, converters=converters)

        if df.empty:
            raise ValueError("File is empty.")
        return df

    @staticmethod
    def validate_required_columns(df: pd.DataFrame, columns: List[str]) -> bool:
        """For each row, verify that all required columns have data."""

        unshared_columns = list(set(columns) - set(df.columns))
        required_columns_diff = len(unshared_columns)

        if required_columns_diff:
            raise ValueError(f"All columns must exist. {unshared_columns} are missing.")

        for column in columns:
            if df[column].isnull().any():
                raise ValueError(f"Column({column}) is missing values.")

        return True

    @staticmethod
    def validate_choice_required_columns(df: pd.DataFrame, columns: List[str]) -> bool:
        """For each row, verify that at least one column has a value."""

        df_subset: pd.DataFrame = df[[*columns]]
        for i, row in df_subset.iterrows():
            if row.isnull().all():
                raise ValueError(
                    f"For Row({i}), at least 1 of Columns({columns}) must have a value."
                )

        return True

    @staticmethod
    def validate_values(
        df: pd.DataFrame, column_name: str, validator: Callable[[pd.Series], bool]
    ) -> bool:
        """For `column`, verify all values are the required format with `validator`."""

        for column_name, column in df[[column_name]].transpose().iterrows():
            if not validator(column):
                raise ValueError(
                    f"Column({column_name}) does not have the required values."
                )

        return True
