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
from program_review_tool.models.ProgramMember.utils import transform_program_member_data_from_external_database

from manager.db.config import EXTERNAL_SOURCE_DATABASE
from manager.services.ldap.provider.utils import fetch_authorized_employee
from manager.settings import ApplicationBuild, BUILD, LDAP_SEARCH_ENDPOINT

LOGGER = logging.getLogger(__name__)

def run():
    try:
        ingest_program_member_data()
    except Exception as exc:
        err_msg = (f"ERROR: cronjob ingest_program_member_data failed: {exc}")
        LOGGER.error(err_msg)
        #TODO: write error to database

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
    if EXTERNAL_SOURCE_DATABASE.lower() == AcceptedExternalDatabases.AXIS:
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

    if df.empty:
        LOGGER.error("No data returned from external source; skipping expiration.")
        return None

    verified_employees = {}
    for employee in set(df["email"]):
        LOGGER.info(f"Verifying ProgramMember: {employee}")
        verified_employees[employee] = fetch_authorized_employee(employee)

    records_to_add: List[models.ProgramMember] = []
    duplicates = set()

    for _, row in df.iterrows():
        program_id: int = int(row["program"])
        role_id: int = int(row["role"])
        user_email: str = row["email"]

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
            & (df["email"].str.lower() == record.user.email.lower())
            & (df["role"] == record.role.id)
        ]
        if filtered_df.empty:
            records_to_expire.append(record.id)
    expiry_date = timezone.now().date()
    models.ProgramMember.objects.filter(id__in=records_to_expire).update(
        expiry_date=expiry_date
    )
    LOGGER.info("Expired: %s ProgramMember records.", len(records_to_expire))

    #TODO: write data to database (who was added, removed, etc)

    return None
