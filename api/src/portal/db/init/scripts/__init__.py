"""
DB init script module. Module accepts a file as an
argument and generates a fixture dataset that may be
be loaded into the application's database using Django
commands such as `loaddata`.
"""

# pylint: disable=logging-fstring-interpolation
import csv
import json
import logging
from typing import List, Tuple
import pandas as pd

from portal.db.init.scripts import fixtures, parser

from manager.settings import BASE_DIR

LOGGER = logging.getLogger(__name__)


class PortalDataFrameColumnValidators:
    """
    Container class for functionality related to
    validating data in `BI Portal` DataFrame columns.
    """

    @staticmethod
    def validate_category(column: pd.Series) -> bool:
        """Verify that column only has the accepted values."""

        accepted_category_values = [
            "command media",
            "excel",
            "powerapps",
            "powerbi",
            "sharepoint",
            "tableau",
            "web link",
        ]

        unaccepted_values = [
            value for value in column if value not in accepted_category_values
        ]
        if len(unaccepted_values) != 0:
            return False
        return True


class PortalFixtureGenerator:
    """Encapsulate logic to generate initial fixtures for `BI Portal`."""

    def __init__(
        self, source: str, sheet_name: str, dest: str, rejected_log: str, err_log: str
    ) -> None:
        self.destination = dest
        self.rejected_log = rejected_log
        self.error_log = err_log

        required_columns = [
            "Function",
            "SubFunction",
            "Display Name",
            "Category",
            "URL",
            "Primary POC",
        ]
        required_choice_columns = ["Employee", "Manager", "Executive"]

        portal_data = parser.Parser.read_file(source, sheet_name)
        parser.Parser.validate_required_columns(portal_data, required_columns)
        parser.Parser.validate_choice_required_columns(
            portal_data, required_choice_columns
        )
        parser.Parser.validate_values(
            portal_data, "Category", PortalDataFrameColumnValidators.validate_category
        )

        self.df = portal_data
        self.users_fixtures = fixtures.Users
        self.request_fixtures = fixtures.Request
        self.directory_fixtures = fixtures.Directory

        self.rejected_rows: List[Tuple[int, str, str]] = []

    def _create_users(self) -> None:
        """Create `User` fixtures objects for `BI Portal`."""

        LOGGER.info("Creating `User` records...")

        internal_users = [
            *self.users_fixtures.User.admins,
            *self.users_fixtures.User.staff,
        ]

        column: List[str] = [
            *list(self.df["Primary POC"].drop_duplicates().str.lower()),
            *internal_users,
        ]
        for email in column:
            try:
                name = email[: email.index("@")].split(".")
                self.users_fixtures.User.add_record(
                    email, name[0].title(), name[-1].title()
                )
            except ValueError as exc:
                LOGGER.error(exc)

        LOGGER.info(
            f"Number of `User` records: {len(self.users_fixtures.User.users['records'])}"
        )

    def _create_accesses(self) -> None:
        """Create `Access` fixtures objects for `BI Portal`."""

        LOGGER.info("Creating `Access` records...")

        internal_users = [
            *self.users_fixtures.User.admins,
        ]

        column: List[str] = [
            *list(self.df["Primary POC"].drop_duplicates().str.lower()),
            *internal_users,
        ]

        for email in column:
            role = (
                self.users_fixtures.Role.AdminRoles.SUPERUSER
                if email in internal_users
                else self.users_fixtures.Role.AdminRoles.DATA_STEWARD
            )
            stages = (
                [
                    self.request_fixtures.Stage.WorkflowStages.SUBMITTED,
                    self.request_fixtures.Stage.WorkflowStages.APPROVED_BY_BUSINESS_PROCESS_EXPERT,
                ]
                if email in internal_users
                else []
            )
            try:
                self.users_fixtures.Access.add_access_record(email, role, stages)
            except ValueError as exc:
                LOGGER.error(exc)

        LOGGER.info(
            f"Number of `Access` records: {len(self.users_fixtures.Access.accesses['records'])}"
        )

    def _create_functions(self) -> None:
        """Create `Function` fixtures objects for `BI Portal`."""

        LOGGER.info("Creating `Function` records...")

        functions = self.df[["Function"]].drop_duplicates()
        for _, row in functions.iterrows():
            try:
                self.directory_fixtures.Function.add_function_record(
                    row["Function"], "TBA"
                )
            except ValueError as exc:
                LOGGER.error(exc)

        LOGGER.info(
            "Number of `Function` records: "
            f"{len(self.directory_fixtures.Function.functions['records'])}"
        )

    def _create_subfunctions(self) -> None:
        """Create `SubFunction` fixtures objects for `BI Portal`."""

        LOGGER.info("Creating `SubFunction` records...")

        subfunctions = self.df[["Function", "SubFunction"]].drop_duplicates(
            subset="SubFunction"
        )
        for _, row in subfunctions.iterrows():
            try:
                self.directory_fixtures.SubFunction.add_subfunction_record(
                    row["SubFunction"], "TBA", row["Function"]
                )
            except ValueError as exc:
                LOGGER.error(exc)

        LOGGER.info(
            "Number of `SubFunction` records: "
            f"{len(self.directory_fixtures.SubFunction.subfunctions['records'])}"
        )

    def _create_tags(self) -> None:
        """Create general `Tag` fixtures objects for `BI Portal`."""

        LOGGER.info("Creating general `Tag` records...")

        tags = set()
        for _, row in self.df[["Tags"]].dropna().iterrows():
            values = str(row["Tags"]).split(",")
            tag_values = [
                value.strip().lower() for value in values if len(value.strip())
            ]
            tags |= set(tag_values)

        tag_count = 0
        for tag in tags:
            try:
                self.directory_fixtures.Tag.add_tag_record(tag)
                tag_count += 1
            except ValueError as exc:
                LOGGER.error(exc)

        LOGGER.info(f"Number of `Tags` records: {tag_count}")

    def _create_site_filter_tags(self) -> None:
        """Create filter `Tag` fixtures objects for `BI Portal`."""

        LOGGER.info("Creating site `Tag` records...")

        tags = set()
        for _, row in self.df[["Site"]].dropna().iterrows():
            values = str(row["Site"]).split(",")
            tag_values = [
                value.strip().lower() for value in values if len(value.strip())
            ]
            tags |= set(tag_values)

        tag_count = 0
        for tag in tags:
            try:
                self.directory_fixtures.Tag.add_tag_record(tag, "filter", "site")
                tag_count += 1
            except ValueError as exc:
                LOGGER.error(exc)

        LOGGER.info(f"Number of Site `Tags` records: {tag_count}")

    def _create_restricted_tags(self) -> None:
        """Create restricted `Tag` fixtures objects for `BI Portal`."""

        LOGGER.info("Creating restricted `Tag` records...")

        tags = set()
        for _, row in self.df[["Restricted"]].dropna().iterrows():
            values = str(row["Restricted"]).split(",")
            tag_values = [
                value.strip().lower() for value in values if len(value.strip())
            ]
            tags |= set(tag_values)

        tag_count = 0
        for tag in tags:
            try:
                self.directory_fixtures.Tag.add_tag_record(
                    tag, "restricted", "jobFunction"
                )
                tag_count += 1
            except ValueError as exc:
                LOGGER.error(exc)

        LOGGER.info(f"Number of Restricted `Tags` records: {tag_count}")

    def _create_resources(self) -> None:
        """Create `Resource` fixtures objects for `BI Portal`."""

        LOGGER.info("Creating `Resource` records...")

        for i, row in self.df.iterrows():
            try:
                subfunctions = (
                    self.df[
                        (self.df["Display Name"] == row["Display Name"])
                        & (self.df["URL"] == row["URL"])
                    ][["SubFunction"]]
                    .drop_duplicates()["SubFunction"]
                    .to_list()
                )

                employee_levels = []
                if row["Employee"] == "X":
                    employee_levels.append("Employee")
                if row["Manager"] == "X":
                    employee_levels.append("Manager")
                if row["Executive"] == "X":
                    employee_levels.append("Executive")

                tags = set()
                if isinstance(row["Tags"], str):
                    values = str(row["Tags"]).split(",")
                    tag_values = [
                        value.strip().lower() for value in values if len(value.strip())
                    ]
                    tags |= set(tag_values)

                if isinstance(row["Site"], str):
                    values = str(row["Site"]).split(",")
                    tag_values = [
                        f"filter::site:{value.strip().lower()}"
                        for value in values
                        if len(value.strip())
                    ]
                    tags |= set(tag_values)

                if isinstance(row["Restricted"], str):
                    values = str(row["Restricted"]).split(",")
                    tag_values = [
                        f"restricted::jobFunction:{value.strip().lower()}"
                        for value in values
                        if len(value.strip())
                    ]
                    tags |= set(tag_values)

                self.directory_fixtures.Resource.add_resource_record(
                    row["Display Name"],
                    row["Description"],
                    row["URL"],
                    employee_levels,
                    subfunctions,
                    list(tags),
                    str(row["Category"]).lower(),
                    False,
                )
            except ValueError as exc:
                LOGGER.info(exc)
                self.rejected_rows.append((i, row["Display Name"], str(exc)))

        LOGGER.info(
            "Number of `Resource` records: "
            f"{len(self.directory_fixtures.Resource.resources['records'])}"
        )

    def _create_requests(self) -> None:
        """Create `Request` fixtures objects for `BI Portal`."""

        LOGGER.info("Creating `Request` records...")

        for _, row in self.df.iterrows():
            try:
                self.request_fixtures.Request.add_request_record(
                    row["Display Name"], str(row["Primary POC"]).lower()
                )
            except ValueError as exc:
                LOGGER.error(exc)

        LOGGER.info(
            "Number of `Request` records: "
            f"{len(self.request_fixtures.Request.requests['records'])}"
        )

    def _create_transitions(self) -> None:
        """Create `Transition` fixtures objects for `BI Portal`."""

        LOGGER.info("Creating `Transition` records...")

        for _, row in self.df.iterrows():
            try:
                self.request_fixtures.Transition.add_transition_record(
                    row["Display Name"],
                    self.request_fixtures.Stage.WorkflowStages.DRAFT,
                )
                self.request_fixtures.Transition.add_transition_record(
                    row["Display Name"],
                    self.request_fixtures.Stage.WorkflowStages.SUBMITTED,
                )
                self.request_fixtures.Transition.add_transition_record(
                    row["Display Name"],
                    self.request_fixtures.Stage.WorkflowStages.APPROVED_BY_SUPERUSER,
                )
            except ValueError as exc:
                LOGGER.error(exc)

        LOGGER.info(
            "Number of `Transition` records: "
            f"{len(self.request_fixtures.Transition.transitions['records'])}"
        )

    def _create_dispositions(self) -> None:
        """Create `Dispositions` fixtures objects for `BI Portal`."""

        LOGGER.info("Creating `Disposition` records...")

        for _, row in self.df.iterrows():
            try:
                self.request_fixtures.Disposition.add_disposition_record(
                    row["Display Name"],
                    self.request_fixtures.Stage.WorkflowStages.SUBMITTED,
                    (
                        self.users_fixtures.User.admins[0]
                        if str(row["Primary POC"]).lower()
                        != self.users_fixtures.User.admins[0]
                        else self.users_fixtures.User.admins[1]
                    ),
                )
            except ValueError as exc:
                LOGGER.error(exc)

        LOGGER.info(
            "Number of `Disposition` records: "
            f"{len(self.request_fixtures.Disposition.dispositions['records'])}"
        )

    def generate_fixtures(self) -> None:
        """Create fixture dataset from the provided .csv/.xls/.xlsx file."""

        LOGGER.info("Generating Fixtures...")

        self._create_users()
        self._create_accesses()
        self._create_functions()
        self._create_subfunctions()
        self._create_tags()
        self._create_site_filter_tags()
        self._create_restricted_tags()

        self._create_resources()

        self._create_requests()
        self._create_transitions()
        self._create_dispositions()

        fixture_data = [
            *self.users_fixtures.Role.roles["records"],
            *self.users_fixtures.User.users["records"],
            *self.users_fixtures.Access.accesses["records"],
            *self.directory_fixtures.EmployeeLevel.employee_levels["records"],
            *self.directory_fixtures.Function.functions["records"],
            *self.directory_fixtures.SubFunction.subfunctions["records"],
            *self.directory_fixtures.Tag.tags["records"],
            *self.directory_fixtures.Resource.resources["records"],
            *self.request_fixtures.Stage.stages["records"],
            *self.request_fixtures.Request.requests["records"],
            *self.request_fixtures.Transition.transitions["records"],
            *self.request_fixtures.Disposition.dispositions["records"],
        ]

        with open(self.destination, "w", encoding="ascii") as fp:
            json.dump(fixture_data, fp, indent=2)

        if len(self.rejected_rows) > 0:
            indexes = [val[0] for val in self.rejected_rows]
            filtered_df = self.df[self.df.index.isin(indexes)]
            filtered_df.to_excel(self.rejected_log)
            LOGGER.info(f"Number of Rejected `Resource` records: {len(indexes)}")
            with open(self.error_log, "w", encoding="ascii") as fp:
                writer = csv.writer(fp)
                writer.writerow(("index", "name", "error"))
                for row in self.rejected_rows:
                    writer.writerow(row)


def run(*args: str) -> None:
    """
    Runscript to create initial fixture dataset with provided excel file.
    It may be invoked from the terminal with the following command:

    `docker-compose exec api python manage.py runscript portal.db.init.scripts
    --script-args /path/to/file <sheet_name>`

    Excel file must have the extension: .csv, .xls, or .xlsx
    """

    LOGGER.info("Parsing Excel file...")

    try:
        file_path = args[0]
        sheet_name = args[1]
        out_path = "portal/db/init/data/init.json"
        rejected_log = "portal/db/init/data/errors/rejected_rows.xlsx"
        error_log = "portal/db/init/data/errors/error_log.csv"
        generator = PortalFixtureGenerator(
            file_path, sheet_name, out_path, rejected_log, error_log
        )
    except ValueError as exc:
        LOGGER.error(f"Parsing Failed. {exc} Please fix issues...")
        return None

    generator.generate_fixtures()
