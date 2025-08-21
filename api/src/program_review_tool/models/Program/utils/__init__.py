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

from django.db import DatabaseError
from django.utils import timezone

from program_review_tool.models import Program
from users.models.Segment.Segment import AR, CS, IMS, SAS, Segment

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

    return (
        round(contract_value)
        if contract_value is not None and not pd.isnull(contract_value)
        else None
    )


def transform_active_status(status: str) -> bool:
    """Given a status as a string, return a boolean indicating
    whether the status is active(True) or inactive(False)."""

    return str(status).lower() in {"active", "o", "l", "y", "yes"}


def query_programs_from_axis(pa_numbers: List[str] | None = None) -> List[dict]:
    """Query program data from `AXIS` given a set of pa numbers."""

    try:
        conn = ExternalDatabaseConnector("axis")
        sql = "SELECT * FROM program"
        if pa_numbers:
            sql = f"{sql} WHERE pa_number IN {tuple(pa_numbers)}"
        df = conn.query_db(sql=sql)
        df["segment"] = df["segment"].apply(transform_segments)
        df["contract_value"] = df["contract_value"].apply(transform_contract_value)
        records: List[dict] = df.to_dict("records")
        return records
    except Exception as exc:
        LOGGER.error(f"Failed to fetch records from AXIS: {exc}")
        return []


def query_programs_from_fdw(pa_numbers: List[str] | None = None) -> List[dict]:
    """Query program data from `FDW` given a set of pa numbers."""

    try:
        conn = ExternalDatabaseConnector("fdw")
        base_sql = """
                SELECT bcom.PROJECT_ID AS pa_number,
                    bcom.PROGRAM_NAME AS program_name,
                    bcom.SEGMENT AS segment,
                    bcom.SECTOR AS sector,
                    bcom.DIVISION AS division,
                    bcom.PROGRAM_TIER AS tier,
                    ppv.CONTRACT_TYPE AS contract_type,
                    ppv.CONTRACT_NUMBER AS contract_number,
                    bcom.CV AS contract_value,
                    ppv.CONTRACT_START_DATE AS contract_start_date,
                    ppv.CONTRACT_END_DATE AS contract_end_date,
                    ppv.CUM_ACWP AS actual_cost_work_performed_cum,
                    ppv.CUM_BCWP AS budget_cost_work_performed_cum,
                    ppv.CUM_BCWS AS budget_cost_work_scheduled_cum,
                    ppv.CUM_CPI_CURRENT AS cost_performance_index_cum,
                    ppv.CUM_SPI_CURRENT AS schedule_performance_index_cum,
                    ppv.BAC AS budget_at_complete,
                    ppv.EAC AS estimate_at_complete,
                    ppv.ETC AS estimate_to_complete,
                    ppv.MANAGEMENT_RESERVE AS management_reserve,
                    ppv.WEIGHTED_RO AS weighted_risks_opportunities,
                    bcom.ACTIVEINACTIVE AS active_status
                FROM BUSANA.BA_CONTRACT_ORG_MASTER bcom
                LEFT JOIN BUSANA.PROGRAM_PERFORMANCE_VIEW ppv
                ON bcom.PROJECT_ID = ppv.PA
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

        # Rename columns appropriately.
        df = df.rename(
            columns={
                "actual_cost_work_performed_cum": "actual_cost_work_performed_cumulative",
                "budget_cost_work_performed_cum": "budgeted_cost_work_performed_cumulative",
                "budget_cost_work_scheduled_cum": "budgeted_cost_work_scheduled_cumulative",
                "cost_performance_index_cum": "cost_performance_index_cumulative",
                "schedule_performance_index_cum": "schedule_performance_index_cumulative",
                "weighted_risks_opportunities": "weighted_risks_and_opportunities",
            }
        )

        EMPTY_STRING_COLUMNS = (
            "pa_number",
            "sector",
            "division",
            "contract_type",
            "contract_number",
        )
        EMPTY_NONE_COLUMNS = (
            "segment",
            "tier",
            "contract_value",
            "contract_start_date",
            "contract_end_date",
            "actual_cost_work_performed_cumulative",
            "budgeted_cost_work_performed_cumulative",
            "budgeted_cost_work_scheduled_cumulative",
            "cost_performance_index_cumulative",
            "schedule_performance_index_cumulative",
            "budget_at_complete",
            "estimate_at_complete",
            "estimate_to_complete",
            "management_reserve",
            "weighted_risks_and_opportunities",
        )

        # Format empty values to empty strings.
        for column in EMPTY_STRING_COLUMNS:
            df[column] = df[column].apply(lambda val: "" if pd.isnull(val) else val)

        # Format empty values to None.
        for column in EMPTY_NONE_COLUMNS:
            df[column] = df[column].apply(lambda val: None if pd.isnull(val) else val)

        ROUNDED_NUMBER_COLUMNS = (
            "actual_cost_work_performed_cumulative",
            "budgeted_cost_work_performed_cumulative",
            "budgeted_cost_work_scheduled_cumulative",
            "cost_performance_index_cumulative",
            "schedule_performance_index_cumulative",
            "budget_at_complete",
            "estimate_at_complete",
            "estimate_to_complete",
            "management_reserve",
            "weighted_risks_and_opportunities",
        )

        for column in ROUNDED_NUMBER_COLUMNS:
            df[column] = df[column].apply(
                lambda value: (
                    round(value, 2)
                    if value is not None and not pd.isnull(value)
                    else None
                )
            )

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
            segment=(
                Segment.objects.get(id=record["segment"]) if record["segment"] else None
            ),
            sector=record["sector"],
            division=record["division"],
            tier=record["tier"],
            contract_type=record["contract_type"],
            contract_number=record["contract_number"],
            contract_value=record["contract_value"],
            contract_start_date=record["contract_start_date"],
            contract_end_date=record["contract_end_date"],
            actual_cost_work_performed_cumulative=record[
                "actual_cost_work_performed_cumulative"
            ],
            budgeted_cost_work_performed_cumulative=record[
                "budgeted_cost_work_performed_cumulative"
            ],
            budgeted_cost_work_scheduled_cumulative=record[
                "budgeted_cost_work_scheduled_cumulative"
            ],
            cost_performance_index_cumulative=record[
                "cost_performance_index_cumulative"
            ],
            schedule_performance_index_cumulative=record[
                "schedule_performance_index_cumulative"
            ],
            budget_at_complete=record["budget_at_complete"],
            estimate_at_complete=record["estimate_at_complete"],
            estimate_to_complete=record["estimate_to_complete"],
            management_reserve=record["management_reserve"],
            weighted_risks_and_opportunities=record["weighted_risks_and_opportunities"],
            active_status=record["active_status"],
            modified=timezone.now(),
        )

    return None


def ingest_new_programs_from_external_database() -> None:
    """Ingest `Program` data from an external database."""

    existing_pa_numbers: List[str] = list(
        Program.objects.values_list("pa_number", flat=True)
    )

    existing_program_names: List[str] = list(
        Program.objects.values_list("name", flat=True)
    )

    records: List[dict] = []
    if EXTERNAL_SOURCE_DATABASE.lower() == AcceptedExternalDatabases.AXIS or BUILD in {
        ApplicationBuild.DEVELOPMENT,
        ApplicationBuild.TEST,
    }:
        records = query_programs_from_axis([])
    elif EXTERNAL_SOURCE_DATABASE.lower() == AcceptedExternalDatabases.FDW:
        records = query_programs_from_fdw([])

    programs_to_ingest: List[Program] = []

    segments = Segment.objects.using("prt").all()

    LOGGER.info(f"Retrieved {len(records)} from the external database.")
    for record in records:
        if (
            record["active_status"]
            and record["pa_number"] not in existing_pa_numbers
            and record["program_name"] not in existing_program_names
        ):
            programs_to_ingest.append(
                Program(
                    pa_number=record["pa_number"],
                    name=record["program_name"],
                    segment=(
                        segments.filter(id=record["segment"]).first()
                        if record["segment"] is not None
                        and not pd.isnull(record["segment"])
                        else None
                    ),
                    sector=record["sector"],
                    division=record["division"],
                    tier=record["tier"],
                    contract_type=record["contract_type"],
                    contract_number=record["contract_number"],
                    contract_value=record["contract_value"],
                    contract_start_date=record["contract_start_date"],
                    contract_end_date=record["contract_end_date"],
                    actual_cost_work_performed_cumulative=record[
                        "actual_cost_work_performed_cumulative"
                    ],
                    budgeted_cost_work_performed_cumulative=record[
                        "budgeted_cost_work_performed_cumulative"
                    ],
                    budgeted_cost_work_scheduled_cumulative=record[
                        "budgeted_cost_work_scheduled_cumulative"
                    ],
                    cost_performance_index_cumulative=record[
                        "cost_performance_index_cumulative"
                    ],
                    schedule_performance_index_cumulative=record[
                        "schedule_performance_index_cumulative"
                    ],
                    budget_at_complete=record["budget_at_complete"],
                    estimate_at_complete=record["estimate_at_complete"],
                    estimate_to_complete=record["estimate_to_complete"],
                    management_reserve=record["management_reserve"],
                    weighted_risks_and_opportunities=record[
                        "weighted_risks_and_opportunities"
                    ],
                    active_status=record["active_status"],
                    created=timezone.now(),
                    modified=timezone.now(),
                )
            )

    failed_ingested_programs = []
    ingestion_count = 0
    for program in programs_to_ingest:
        try:
            program.save()
            ingestion_count += 1
        except DatabaseError:
            failed_ingested_programs.append(f"{program.pa_number} - {program.name}")

    LOGGER.info(f"Ingested {ingestion_count} new programs.")

    if len(failed_ingested_programs):
        LOGGER.error(
            f"Failed to ingest {len(failed_ingested_programs)} programs. {failed_ingested_programs}"
        )

    return None
