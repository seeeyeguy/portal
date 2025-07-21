"""
`Program` model utils module. Common functionality for
database operations that may affect the `Program` model.
"""

# pylint: disable=logging-fstring-interpolation
import logging
import pandas as pd
import pyodbc as mssqldb  # type: ignore[import-not-found]
from sqlalchemy import create_engine
from typing import List, Union

from program_review_tool.models import Program
from users.models.Segment.Segment import AR, CS, IMS, SAS

from manager.db.config import AXIS, EXTERNAL_SOURCE_DATABASE, FDW
from manager.settings import ApplicationBuild, BUILD

LOGGER = logging.getLogger(__name__)

FDW_WHERE_IN_LIMIT: int = 1000


class AcceptedExternalDatabases:
    """Supported External Databases."""

    AXIS = "axis"
    FDW = "fdw"


class ExternalDatabaseConnector:
    """Class to manage connections to external databases
    and issue SQL queries."""

    def __init__(self, db: str):
        """Initialize a connection to an external database."""

        self.engine = None

        if not hasattr(AcceptedExternalDatabases, db.upper()):
            supported_dbs = [
                attr
                for attr in AcceptedExternalDatabases.__dict__
                if not attr.startswith("__")
            ]
            raise ValueError(f"Only {supported_dbs} are accepted.")

        if db.lower() == AcceptedExternalDatabases.AXIS:
            server = AXIS.HOST
            database = AXIS.NAME
            username = AXIS.USER
            password = AXIS.PASSWORD
            self.engine = mssqldb.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
                + server
                + ";DATABASE="
                + database
                + ";UID="
                + username
                + ";PWD="
                + password
            )

        elif db.lower() == AcceptedExternalDatabases.FDW:
            host = FDW.HOST
            port = FDW.PORT
            database = FDW.NAME
            username = FDW.USER
            password = FDW.PASSWORD
            engine = "oracle+oracledb"
            self.engine = create_engine(
                f"{engine}://{username}:{password}@{host}:{port}/{database}"
            )

    def query_db(self, sql: str) -> pd.DataFrame:
        """Query an external database for records with the provided SQL."""

        return pd.read_sql(sql=sql, con=self.engine)


def transform_segments(segment: str) -> Union[int, None]:
    """Given a segment, return the corresponding primary key
    for that segment in our database."""

    if str(segment).upper() in AR:
        return AR[0]
    if str(segment).upper() in CS:
        return CS[0]
    if str(segment).upper() in IMS:
        return IMS[0]
    if str(segment).upper() in SAS:
        return SAS[0]

    return None


def transform_contract_value(contract_value: float) -> Union[int, None]:
    """Given contract_value as a float, return a rounded int."""

    return round(contract_value) if contract_value is not None else None


def transform_active_status(status: str) -> bool:
    """Given a status as a string, return a boolean indicating
    whether the status is active(True) or inactive(False)."""

    return str(status).lower() in {"active", "o", "l", "y", "yes"}


def query_programs_from_axis(pa_numbers: List[str]) -> List[dict]:
    """Query program data from `AXIS` given a set of pa numbers."""

    try:
        conn = ExternalDatabaseConnector("axis")
        sql = f"SELECT * FROM program WHERE pa_number IN {tuple(pa_numbers)}"
        df = conn.query_db(sql=sql)
        df["segment"] = df["segment"].apply(transform_segments)
        df["contract_value"] = df["contract_value"].apply(transform_contract_value)
        df["active_status"] = df["active_status"].apply(transform_active_status)
        records: List[dict] = df.to_dict("records")
        return records
    except Exception as exc:
        LOGGER.error(f"Failed to fetch records from AXIS: {exc}")
        return []


def query_programs_from_fdw(pa_numbers: List[str]) -> List[dict]:
    """Query program data from `FDW` given a set of pa numbers."""

    try:
        conn = ExternalDatabaseConnector("fdw")
        base_sql = f"""
        SELECT bcom.PROJECT_ID AS pa_number,
            bcom.PROGRAM_NAME AS program_name,
            bcom.SEGMENT AS segment,
            bcom.SECTOR AS sector,
            bcom.DIVISION AS division,
            p.FINAL_TIER AS tier,
            bcom.CV AS contract_value,
            bcom.ACTIVEINACTIVE AS active_status
        FROM BUSANA.BA_CONTRACT_ORG_MASTER bcom
        JOIN
        BUSANA.PROGRAM_TIER p ON p.PA_ID = bcom.PROJECT_ID        
        """

        df = pd.DataFrame()
        if pa_numbers:
            if len(pa_numbers) < FDW_WHERE_IN_LIMIT:
                sql = f"""
                {base_sql}
                WHERE bcom.PROJECT_ID IN {tuple(pa_numbers)}
                """
                df = conn.query_db(sql=sql)
            else:
                i, j = 0, FDW_WHERE_IN_LIMIT
                while i < len(pa_numbers):
                    sql = f"""
                        {base_sql}
                        WHERE bcom.PROJECT_ID IN {tuple(pa_numbers[i:j])}
                        """
                    query_df = conn.query_db(sql=sql)
                    df = pd.concat([df, query_df])

                    i, j = j, j + FDW_WHERE_IN_LIMIT
        else:
            df = conn.query_db(sql=base_sql)

        df = df.loc[
            ~(
                (df["segment"].isnull())
                | (df["sector"].isnull())
                | (df["division"].isnull())
                | (df["tier"].isnull())
                | (df["contract_value"].isnull())
            )
        ]
        df["segment"] = df["segment"].apply(transform_segments)
        df["contract_value"] = df["contract_value"].apply(transform_contract_value)
        df["active_status"] = df["active_status"].apply(transform_active_status)
        records: List[dict] = df.to_dict("records")
        return records
    except Exception as exc:
        LOGGER.error(f"Failed to fetch records from FDW: {exc}")
        return []


def update_programs_from_external_database() -> None:
    """Update `Program` data with that of an external database."""

    existing_pa_numbers: List[str] = list(
        Program.objects.values_list("pa_number", flat=True)
    )

    records: List[dict] = []
    if EXTERNAL_SOURCE_DATABASE.lower() == AcceptedExternalDatabases.AXIS or BUILD in {
        ApplicationBuild.DEVELOPMENT,
        ApplicationBuild.TEST,
    }:
        records = query_programs_from_axis(existing_pa_numbers)
    elif EXTERNAL_SOURCE_DATABASE.lower() == AcceptedExternalDatabases.FDW:
        records = query_programs_from_fdw(existing_pa_numbers)

    for record in records:
        Program.objects.filter(pa_number=record["pa_number"]).update(
            name=record["program_name"],
            segment=record["segment"],
            sector=record["sector"],
            division=record["division"],
            tier=record["tier"],
            contract_value=record["contract_value"],
            active_status=record["active_status"],
        )

    return None
