"""
Collection of pytests for Programs's fetch view endpoint.
"""

import json
from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from program_review_tool import models
from program_review_tool.controllers.Program.tests.query.read.default import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "program",
    "program_review_tool",
    "views",
    "program.fetch.default",
    "program_review_tool.program.fetch",
    "views.TestFetchProgram",
)
class TestFetchProgram(MultiDBTestCase):
    """
    Tests for GET /v1/program-review-tool/program endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Program/tests/query/read/default/fixtures/segments.json",
        "program_review_tool/controllers/Program/tests/query/read/default/fixtures/programs.json",
    ]

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.FETCH_PROGRAMS_USER)
        self.client.force_login(user=user)

        program_fixtures_path: str = "program_review_tool/controllers/Program/tests/query/read/default/fixtures/programs.json"
        with open(
            program_fixtures_path,
            "r",
            encoding="utf-8",
        ) as f:
            self.program_fixtures = json.load(f)

        self.program_fixtures = {
            program["pk"]: {
                **program["fields"],
                "id": program["pk"],
                "segment": "SPACE & AIRBORNE SYSTEMS",
                "team_members": list(
                    models.ProgramMember.objects.filter(
                        program__id=program["pk"], is_active=True
                    )
                ),
            }
            for program in self.program_fixtures
        }

    url: str = reverse("program_review_tool.program")

    @tag("views.program.fetch_programs")
    def test_fetch_programs(self) -> None:
        """Success Case: Fetch active `Program` records."""

        response = self.client.get(
            self.url,
            headers={"content_type": "application/json"},
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(len(programs), len(arguments.FETCH_PROGRAMS_ALL_VALID_IDS))

        for program in programs:
            program_id: int = program["id"]

            self.assertIsInstance(program, dict)

            self.assertIn(program_id, self.program_fixtures)

            expected_program = self.program_fixtures[program_id]

            del program["created"]
            del program["modified"]

            del expected_program["created"]
            del expected_program["modified"]

            self.assertEqual(
                program,
                expected_program,
            )

    @tag("views.program.fetch_programs_with_ids")
    def test_fetch_programs_with_ids(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given ids."""

        program_params: dict = {"ids": arguments.FETCH_PROGRAM_IDS}

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(len(programs), len(arguments.FETCH_PROGRAM_IDS))

        for program in programs:
            program_id: int = program["id"]

            self.assertIsInstance(program, dict)

            self.assertIn(program_id, arguments.FETCH_PROGRAM_IDS)

            expected_program = self.program_fixtures[program_id]

            del program["created"]
            del program["modified"]

            del expected_program["created"]
            del expected_program["modified"]

            self.assertEqual(
                program,
                expected_program,
            )

    @tag("views.program.fetch_programs_with_pa_numbers")
    def test_fetch_programs_with_pa_numbers(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given PA numbers."""

        program_params: dict = {"pa_numbers": arguments.FETCH_PROGRAM_PA_NUMBERS}

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(len(programs), len(arguments.FETCH_PROGRAM_PA_NUMBERS))

        for program in programs:
            program_id: int = program["id"]

            self.assertIsInstance(program, dict)

            self.assertIn(program_id, arguments.FETCH_PROGRAM_IDS)

            expected_program = self.program_fixtures[program_id]

            del program["created"]
            del program["modified"]

            del expected_program["created"]
            del expected_program["modified"]

            self.assertEqual(
                program,
                expected_program,
            )

    @tag("views.program.fetch_programs_with_page")
    def test_fetch_programs_with_page(self) -> None:
        """Success Case: Fetch page of active `Program` records."""

        program_params: dict = {"page": arguments.FETCH_PROGRAM_WITH_PAGE}

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(
            len(programs), arguments.FETCH_PROGRAM_WITH_PAGE_EXPECTED_COUNT
        )

        for program in programs:
            program_id: int = program["id"]

            self.assertIn(program_id, arguments.FETCH_PROGRAM_WITH_PAGE_IDS)

            self.assertIsInstance(program, dict)

            expected_program = self.program_fixtures[program_id]

            del program["created"]
            del program["modified"]

            del expected_program["created"]
            del expected_program["modified"]

            self.assertEqual(
                program,
                expected_program,
            )

    @tag("views.program.fetch_programs_with_limit")
    def test_fetch_programs_with_limit(self) -> None:
        """Success Case: Fetch active `Program` records up to a limit."""

        program_params: dict = {"limit": arguments.FETCH_PROGRAM_WITH_LIMIT}

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(len(programs), arguments.FETCH_PROGRAM_WITH_LIMIT)

    @tag("views.program.fetch_programs_with_page_and_limit")
    def test_fetch_programs_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of active `Program` records up to a limit."""

        program_params: dict = {
            "page": arguments.FETCH_PROGRAM_WITH_PAGE,
            "limit": arguments.FETCH_PROGRAM_WITH_LIMIT,
        }

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(
            len(programs), len(arguments.FETCH_PROGRAM_WITH_PAGE_AND_LIMIT_VALID_IDS)
        )

        for program in programs:
            program_id: int = program["id"]

            self.assertIn(
                program_id, arguments.FETCH_PROGRAM_WITH_PAGE_AND_LIMIT_VALID_IDS
            )

            self.assertIsInstance(program, dict)

            self.assertIn(program_id, self.program_fixtures)

            expected_program = self.program_fixtures[program_id]

            del program["created"]
            del program["modified"]

            del expected_program["created"]
            del expected_program["modified"]

            self.assertEqual(
                program,
                expected_program,
            )

    @tag("views.program.fetch_programs_with_page_exceeding_max_page")
    def test_fetch_programs_with_page_exceeding_max_page(self) -> None:
        """Success Case: Fetch active `Program` records using a
        page number that exceeds the number of pages."""

        program_params: dict = {
            "page": arguments.FETCH_PROGRAM_WITH_PAGE_EXCEEDING_MAX_PAGE_COUNT
        }

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(
            len(programs),
            arguments.FETCH_PROGRAM_WITH_PAGE_EXCEEDING_MAX_PAGE_COUNT_RECORD_COUNT,
        )

    @tag("views.program.fetch_programs_ids_dne")
    def test_fetch_programs_ids_dne(self) -> None:
        """Fail Case: Fetch `Program` records for
        ids that do not exist."""

        program_params: dict = {"ids": arguments.FETCH_PROGRAM_BY_PROGRAM_ID_DNE}

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.program.fetch_programs_pa_numbers_dne")
    def test_fetch_programs_pa_numbers_dne(self) -> None:
        """Fail Case: Fetch `Program` records for
        PA numbers that do not exist."""

        program_params: dict = {
            "pa_numbers": arguments.FETCH_PROGRAM_BY_PROGRAM_PA_NUMBER_DNE
        }

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
