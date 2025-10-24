"""
`ProgramMember` model utils module. Common functionality for
database operations that may affect the `ProgramMember` model.
"""

# pylint: disable=logging-fstring-interpolation
import logging
import pandas as pd
import re
import requests
from typing import cast, List, Optional

from django.db.models import QuerySet
from django.utils import timezone

from program_review_tool.models.Program.utils import (
    AcceptedExternalDatabases,
    ExternalDatabaseConnector,
)
from program_review_tool import models

from manager.db.config import EXTERNAL_SOURCE_DATABASE
from manager.services.ldap.provider.utils import fetch_authorized_employee
from manager.settings import ApplicationBuild, BUILD, LDAP_SEARCH_ENDPOINT

LOGGER = logging.getLogger(__name__)

VALID_PROGRAM_ROLE_VALUES = [
    models.ProgramRole.ProgramRoles.PROGRAM_MANAGER,
    models.ProgramRole.ProgramRoles.PROGRAM_FINANCIAL_ANALYST,
]

PROGRAM_ROLE_TO_EXTERNAL_DATABASE_ROLE_MAPPING = {
    models.ProgramRole.ProgramRoles.PROGRAM_MANAGER: ("PM", "PGM"),
    models.ProgramRole.ProgramRoles.PROGRAM_FINANCIAL_ANALYST: ("PFA",),
}


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to standard naming conventions,
    and drop the status column if it exists."""

    df = df.rename(
        columns={
            "project_id": "pa_number",
            "descr": "description",
            "support_team_member": "employee_id",
            "email_address": "email",
        }
    )

    df = df.drop(columns=["status"])

    return df


def transform_pa_number_to_program_id(df: pd.DataFrame) -> pd.DataFrame:
    """Add a `Program` id column using the given pa numbers within the `DataFrame`,
    drop any rows where a related program id cannot be found, and drop the pa number
    column."""

    programs = models.Program.objects.only("id", "pa_number").all()
    pa_number_mapping: dict[str, Optional[int]] = {}

    transformed_df = df.copy()

    transformed_df = transformed_df.dropna(subset=["pa_number"])
    transformed_df["pa_number"] = transformed_df["pa_number"].str.upper()

    def get_program_id(pa_number: str) -> Optional[int]:
        if pa_number.upper() in pa_number_mapping:
            return pa_number_mapping[pa_number.upper()]
        program = programs.filter(pa_number__iexact=pa_number).first()
        pa_number_mapping[pa_number.upper()] = (
            program.id if program is not None else None
        )
        return pa_number_mapping[pa_number.upper()]

    transformed_df["program"] = df["pa_number"].apply(get_program_id)
    transformed_df = transformed_df.dropna(subset=["program"])
    transformed_df = transformed_df.drop(columns=["pa_number"])

    return transformed_df


def extract_last_name_from_name(name: str) -> str:
    """Extract a last name from a given full name, using
    a regex to account for expected spacing, punctuation,
    and suffixes."""

    pattern = r"(.*?)(\s)?(Jr|I{2}I?)?(\s|,)(.*)"
    match = re.search(pattern, name)

    return match.group(1) if match else ""


def extract_first_name_from_name(name: str) -> str:
    """Extract a first name from a given full name, using
    a regex to account for expected spacing, punctuation,
    suffixes, and a potential middle initial."""

    pattern = r"(.*?)(\s)?(Jr|I{2}I?)?(\s|,)(.*)"
    match = re.search(pattern, name)

    return match.group(5).split(" ")[0].strip() if match else ""


def create_mapping_from_full_names_to_emails(df: pd.DataFrame) -> pd.DataFrame:
    """Create a mapping from an employee's full name to an email address given
    a dataframe containing employees without associated email addresses."""

    name_to_email_mapping: dict[str, Optional[str]] = {}

    missing_employee_emails_df = df[df["email"].isnull()]
    missing_employee_emails_df = missing_employee_emails_df.drop_duplicates(
        ["full_name"]
    )
    for name in missing_employee_emails_df["full_name"]:
        payload = {
            "search_term": name,
            "limit": 1,
            "offset": 1,
        }

        response = requests.post(LDAP_SEARCH_ENDPOINT, payload)

        if not response.ok:
            name_to_email_mapping[name] = None
        else:
            results = cast(dict, response.json())
            entries = cast(list, results["entries"])
            if not entries:
                name_to_email_mapping[name] = None
            else:
                name_to_email_mapping[name] = entries[0]["email"]

    return name_to_email_mapping


def populate_emails_using_transformed_employee_data(df: pd.DataFrame) -> pd.DataFrame:
    """Using full names extracted from employee name, populate dataframe with associated
    emails from LDAP if they exist."""

    output = df.copy()

    output["last_name"] = output["name"].apply(extract_last_name_from_name)
    output["first_name"] = output["name"].apply(extract_first_name_from_name)
    output["full_name"] = output["first_name"] + " " + output["last_name"]

    email_mapping = create_mapping_from_full_names_to_emails(output)
    output["email"] = output.apply(
        lambda row: email_mapping.get(row["full_name"], row["email"]), axis=1
    )
    output["email"] = output["email"].apply(
        lambda e: e.lower() if isinstance(e, str) else e
    )

    output = output.dropna(subset=["email"])

    return output


def transform_role_name_into_foreign_key_reference(role: str) -> Optional[int]:
    """Helper function to transform `ProgramRole` name data from external data
    source to its foreign key reference."""

    if (
        role
        in PROGRAM_ROLE_TO_EXTERNAL_DATABASE_ROLE_MAPPING[
            models.ProgramRole.ProgramRoles.PROGRAM_MANAGER
        ]
    ):
        return models.ProgramRole.ProgramRoles.PROGRAM_MANAGER
    if (
        role
        in PROGRAM_ROLE_TO_EXTERNAL_DATABASE_ROLE_MAPPING[
            models.ProgramRole.ProgramRoles.PROGRAM_FINANCIAL_ANALYST
        ]
    ):
        return models.ProgramRole.ProgramRoles.PROGRAM_FINANCIAL_ANALYST

    return None


def transform_roles_in_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Transform `ProgramRole` data in DataFrame from external data
    source to its foreign key reference."""

    transformed_df = df.copy()
    transformed_df["role"] = transformed_df["role"].apply(
        transform_role_name_into_foreign_key_reference
    )
    transformed_df = transformed_df.dropna(subset=["role"])

    return transformed_df


def query_program_members_from_external_database(
    data_source: str, pa_number: Optional[str] = None, role: Optional[int] = None
) -> pd.DataFrame:
    """Query program team member data from an external database."""

    if not hasattr(AcceptedExternalDatabases, data_source):
        LOGGER.error(f"{data_source} is not an accepted database.")
        raise ValueError(f"{data_source} is not an accepted database.")

    if role and role not in VALID_PROGRAM_ROLE_VALUES:
        LOGGER.error(
            f"{role} must be a value specified within `ProgramRole.ProgramRoles`."
        )
        raise ValueError(
            f"{role} must be a value specified within `ProgramRole.ProgramRoles`."
        )

    conn = ExternalDatabaseConnector(data_source.lower())

    base_sql = ""
    if data_source.lower() == AcceptedExternalDatabases.FDW:
        base_sql = """
            SELECT  ptm.project_id,
                    ptm.role,
                    ptm.descr,
                    ptm.support_team_member,
                    emc.email_address, 
                    emc.name,
                    emc.status
            FROM BUSANA.PROGRAM_TEAM_MEMBERS ptm
            JOIN BUSANA.EMPLOYEE_MASTER_CURRENT emc
            ON ptm.support_team_member = emc.eid WHERE emc.status = 'A'
        """

        if pa_number and role:
            base_sql = f"""
            {base_sql} AND ptm.PROJECT_ID = '{pa_number}' AND ptm.ROLE IN
            {PROGRAM_ROLE_TO_EXTERNAL_DATABASE_ROLE_MAPPING[role]}
            """
        elif pa_number:
            base_sql = f"""
            {base_sql} AND ptm.PROJECT_ID = '{pa_number}'
            """
        elif role:
            base_sql = f"""
            {base_sql} AND ptm.ROLE IN {PROGRAM_ROLE_TO_EXTERNAL_DATABASE_ROLE_MAPPING[role]}
            """
    else:
        base_sql = """"""

    df = conn.query_db(sql=base_sql)

    return df


def transform_program_member_data_from_external_database(
    data_source: str, pa_number: Optional[str] = None, role: Optional[int] = None
) -> pd.DataFrame:
    """Transform queried data from external database to be ingested into
    `ProgramMember` table."""

    df = query_program_members_from_external_database(
        data_source=data_source, pa_number=pa_number, role=role
    )

    df = normalize_column_names(df)
    df = transform_pa_number_to_program_id(df)
    df = transform_roles_in_dataframe(df)
    df = populate_emails_using_transformed_employee_data(df)
    df = df.assign(expiry_date=None, created=timezone.now())

    return df


def ingest_program_member_data() -> Optional[int]:
    """Ingest `ProgramMember` data from an external database."""

    LOGGER.info("Starting ingestion of new Program Members....")

    existing_program_roles = cast(
        dict[int, models.ProgramRole], models.ProgramRole.objects.in_bulk()
    )
    existing_programs = cast(
        dict[int, models.Program], models.Program.objects.in_bulk()
    )
    existing_program_members: QuerySet[
        models.ProgramMember
    ] = models.ProgramMember.objects.all()

    data_source = None
    if EXTERNAL_SOURCE_DATABASE.lower() == AcceptedExternalDatabases.AXIS or BUILD in {
        ApplicationBuild.DEVELOPMENT,
        ApplicationBuild.TEST,
    }:
        data_source = AcceptedExternalDatabases.AXIS.upper()
    elif EXTERNAL_SOURCE_DATABASE.lower() == AcceptedExternalDatabases.FDW:
        data_source = AcceptedExternalDatabases.FDW.upper()

    if not data_source:
        LOGGER.error(
            "Accepted data source was not specified in `.env` `EXTERNAL_SOURCE_DATABASE`."
        )
        raise ValueError(
            "Accepted data source was not specified in `.env` `EXTERNAL_SOURCE_DATABASE`."
        )

    df = transform_program_member_data_from_external_database(data_source=data_source)

    verified_employees = {}
    for employee in set(df["email"]):
        LOGGER.info(f"Verifying ProgramMember: {employee}")
        verified_employees[employee] = fetch_authorized_employee(employee)

    records_to_add: List[models.ProgramMember] = []
    duplicates = set()

    for _, row in df.iterrows():
        program_id: int = int(row["program"])
        role_id: int = int(row["role"])
        # E-mails in the `DataFrame` have the `l3harris.com` domain
        # and need to be converted to `harris.com` domain for the
        # correct verification.
        user_email: str = row["email"].replace("@l3harris.com", "@harris.com")

        # Construct the composite key from the `Program` id,
        # `ProgramRole` id and the `User` email.
        composite_key = (program_id, role_id, user_email)
        if (
            not existing_program_members.filter(
                program__id=program_id,
                role__id=role_id,
                user__email__iexact=user_email,
                expiry_date__isnull=True,
            ).exists()
            and composite_key not in duplicates
        ):
            verified_employee = verified_employees[row["email"]]

            if not verified_employee or not hasattr(verified_employee, "id"):
                LOGGER.info(
                    f"Skipping ProgramMember insert: No valid User found for {row['email']}"
                )
                continue
            if verified_employee:
                try:
                    records_to_add.append(
                        models.ProgramMember(
                            program=existing_programs[program_id],
                            role=existing_program_roles[role_id],
                            user=verified_employee,
                            created=row["created"],
                            expiry_date=None,
                            modified=timezone.now(),
                        )
                    )
                    duplicates.add(composite_key)
                except Exception as exc:
                    err_msg = (
                        f"ERROR: Failed to stage adding ProgramMember for {row['email']} "
                        f"(program={row['program']}, role={row['role']}): {exc}"
                    )
                    LOGGER.error(err_msg)
                    continue
    LOGGER.info("Attempt to Create: %s ProgramMember records.", len(records_to_add))

    models.ProgramMember.objects.bulk_create(records_to_add)

    LOGGER.info("Created: %s ProgramMember records.", len(records_to_add))

    records_to_expire: List[int] = []
    for record in existing_program_members.select_related(
        "program", "user", "role"
    ).filter(expiry_date__isnull=True):
        filtered_df = df.loc[
            (df["program"] == record.program.id)
            & (
                df["email"]
                == record.user.email.replace("@harris.com", "@l3harris.com").lower()
            )
            & (df["role"] == record.role.id)
        ]
        if filtered_df.empty:
            records_to_expire.append(record.id)
    expiry_date = timezone.now().date()
    models.ProgramMember.objects.filter(id__in=records_to_expire).update(
        expiry_date=expiry_date
    )
    LOGGER.info("Expired: %s ProgramMember records.", len(records_to_expire))

    return None
