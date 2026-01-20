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

from program_review_tool.models.Program.serializers import ProgramMemberSerializer

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
        "program_review_tool/controllers/Program/tests/query/read/default/fixtures/programmembers.json",
    ]

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(username=arguments.FETCH_PROGRAMS_USER)
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
                "team_members": ProgramMemberSerializer(
                    models.ProgramMember.objects.filter(
                        program__id=program["pk"], expiry_date__isnull=True
                    ),
                    many=True,
                ).data,
            }
            for program in self.program_fixtures
        }

    url: str = reverse("program_review_tool.program")

    @tag("views.program.fetch_programs")
    def test_fetch_programs(self) -> None:
        """Success Case: Fetch `Program` records."""

        program_params: dict = {"active_only": False}

        response = self.client.get(
            self.url, program_params, content_type="application/json"
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

    @tag("views.program.fetch_active_programs")
    def test_fetch_active_programs(self) -> None:
        """Success Case: Fetch active `Program` records."""

        response = self.client.get(
            self.url,
            headers={"content_type": "application/json"},
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(
            len(programs), len(arguments.FETCH_PROGRAMS_ALL_ACTIVE_VALID_IDS)
        )

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

    @tag("views.program.fetch_programs_by_tiers")
    def test_fetch_programs_by_tiers(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given tiers."""

        program_params: dict = {
            "tiers": arguments.FETCH_PROGRAMS_BY_TIERS_TIERS,
        }

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(
            len(programs), len(arguments.FETCH_PROGRAMS_BY_TIERS_VALID_IDS)
        )

        for program in programs:
            program_id: int = program["id"]

            self.assertIn(program_id, arguments.FETCH_PROGRAMS_BY_TIERS_VALID_IDS)

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

    @tag("views.program.fetch_programs_by_program_member")
    def test_fetch_programs_by_program_member(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given `ProgramMember`'s `User` email."""

        program_params: dict = {
            "program_member": arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_USER_EMAIL,
        }

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(
            len(programs), len(arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_VALID_IDS)
        )

        for program in programs:
            program_id: int = program["id"]

            self.assertIn(
                program_id, arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_VALID_IDS
            )

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

    @tag("views.program.fetch_programs_by_program_member_no_program_member")
    def test_fetch_programs_by_program_member_no_program_member(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given `ProgramMember`'s `User` email, where the `User` does not
        have an active `ProgramMember` entry."""

        program_params: dict = {
            "program_member": arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_NO_ACTIVE_PROGRAM_MEMBER_USER_EMAIL,
        }

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(
            len(programs),
            arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_NO_ACTIVE_PROGRAM_MEMBER_PROGRAM_COUNT,
        )

    @tag("views.program.fetch_programs_by_tiers_and_program_member")
    def test_fetch_programs_by_tiers_and_program_member(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given tiers and `ProgramMember`'s `User` email."""

        program_params: dict = {
            "tiers": arguments.FETCH_PROGRAMS_BY_TIERS_AND_PROGRAM_MEMBER_TIERS,
            "program_member": arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_USER_EMAIL,
        }

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        programs = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(programs, list)

        self.assertEqual(
            len(programs),
            len(arguments.FETCH_PROGRAMS_BY_TIERS_AND_PROGRAM_MEMBER_VALID_IDS),
        )

        for program in programs:
            program_id: int = program["id"]

            self.assertIn(
                program_id,
                arguments.FETCH_PROGRAMS_BY_TIERS_AND_PROGRAM_MEMBER_VALID_IDS,
            )

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

    @tag("views.program.fetch_programs_by_ids_and_pa_numbers")
    def test_fetch_programs_by_ids_and_pa_numbers(self) -> None:
        """Fail Case: Fetch `Program` records for
        by both ids and PA numbers."""

        program_params: dict = {
            "ids": arguments.FETCH_PROGRAM_IDS,
            "pa_numbers": arguments.FETCH_PROGRAM_PA_NUMBERS,
        }

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    @tag("views.program.fetch_programs_program_member_user_dne")
    def test_fetch_programs_program_member_user_dne(self) -> None:
        """Fail Case: Fetch `Program` records for
        a `ProgramMember` `User` that does not exist."""

        program_params: dict = {
            "program_member": arguments.FETCH_PROGRAMS_PROGRAM_MEMBER_USER_DNE_EMAIL
        }

        response = self.client.get(
            self.url, program_params, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
