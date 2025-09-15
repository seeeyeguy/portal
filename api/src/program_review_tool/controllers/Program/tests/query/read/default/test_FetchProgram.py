"""
Collection of pytests for Program's fetch controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import json
import pytest
from typing import List

from django.db.models import QuerySet
from django.test import tag

from program_review_tool import controllers, exceptions, models
from program_review_tool.controllers.Program.tests.query.read.default import arguments
from program_review_tool.models.Program.serializers import (
    ProgramSerializer,
    ProgramMemberSerializer,
)

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "program",
    "program_review_tool",
    "controllers.TestFetchProgram",
    "program.fetch.default",
    "program_review_tool.program.fetch",
)
class TestFetchProgram(MultiDBTestCase):
    """Test suite for Program's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Program/tests/query/read/default/fixtures/segments.json",
        "program_review_tool/controllers/Program/tests/query/read/default/fixtures/programs.json",
        "program_review_tool/controllers/Program/tests/query/read/default/fixtures/programmembers.json",
    ]

    def setUp(self) -> None:
        super().setUp()

        program_fixtures_path: str = "program_review_tool/controllers/Program/tests/query/read/default/fixtures/programs.json"
        with open(
            program_fixtures_path,
            "r",
            encoding="utf-8",
        ) as f:
            self.program_fixtures = json.load(f)

        self.program_fixtures = {
            program["pk"]: {
                **{
                    k: v
                    for k, v in program["fields"].items()
                    if k not in ("segment", "created", "modified")
                },
                "id": program["pk"],
                "team_members": ProgramMemberSerializer(
                    models.ProgramMember.objects.filter(
                        program__id=program["pk"], expiry_date__isnull=True
                    ),
                    many=True,
                ).data,
            }
            for program in self.program_fixtures
        }

    @tag("controllers.program.fetch_programs")
    def test_fetch_programs(self) -> None:
        """Success Case: Fetch active `Program` records."""

        programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
            program_ids=[],
            pa_numbers=[],
            tiers=[],
            program_member="",
            page=None,
            limit=None,
        )

        self.assertIsInstance(programs, QuerySet[models.Program])

        self.assertEqual(
            programs.filter(id__in=arguments.FETCH_PROGRAMS_ALL_VALID_IDS).count(),
            len(arguments.FETCH_PROGRAMS_ALL_VALID_IDS),
        )

        for program in programs:
            self.assertIsInstance(program, models.Program)

            program_id: int = program.id

            self.assertIn(program_id, self.program_fixtures)

            serialized_program = ProgramSerializer(program).data
            expected_program = self.program_fixtures[program_id]

            del serialized_program["segment"]
            del serialized_program["created"]
            del serialized_program["modified"]

            self.assertEqual(
                serialized_program,
                expected_program,
            )

    @tag("controllers.program.fetch_programs_with_ids")
    def test_fetch_programs_with_ids(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given ids."""

        programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
            program_ids=arguments.FETCH_PROGRAM_IDS,
            pa_numbers=[],
            page=None,
            limit=None,
        )

        self.assertIsInstance(programs, QuerySet[models.Program])

        data: dict = ProgramSerializer(programs, many=True).data

        self.assertEqual(
            data, list(arguments.EXPECTED_PROGRAMS_PROGRAM_ID_VALIDATE_PARAMS.values())
        )

    @tag("controllers.program.fetch_programs_with_pa_numbers")
    def test_fetch_programs_with_pa_numbers(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given PA numbers."""

        programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
            program_ids=[],
            pa_numbers=arguments.FETCH_PROGRAM_PA_NUMBERS,
            tiers=[],
            program_member="",
            page=None,
            limit=None,
        )

        self.assertIsInstance(programs, QuerySet[models.Program])

        data: dict = ProgramSerializer(programs, many=True).data

        self.assertEqual(
            data, list(arguments.EXPECTED_PROGRAMS_PROGRAM_ID_VALIDATE_PARAMS.values())
        )

    @tag("controllers.program.fetch_programs_by_tiers")
    def test_fetch_programs_by_tiers(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given tiers."""

        programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
            program_ids=[],
            pa_numbers=[],
            tiers=arguments.FETCH_PROGRAMS_BY_TIERS_TIERS,
            program_member="",
            page=None,
            limit=None,
        )

        self.assertIsInstance(programs, QuerySet[models.Program])

        self.assertEqual(
            programs.count(), len(arguments.FETCH_PROGRAMS_BY_TIERS_VALID_IDS)
        )

        for program in programs:
            self.assertIsInstance(program, models.Program)

            program_id: int = program.id

            self.assertIn(program_id, self.program_fixtures)
            self.assertIn(program_id, arguments.FETCH_PROGRAMS_BY_TIERS_VALID_IDS)

            serialized_program = ProgramSerializer(program).data
            expected_program = self.program_fixtures[program_id]

            del serialized_program["segment"]
            del serialized_program["created"]
            del serialized_program["modified"]

            self.assertEqual(
                serialized_program,
                expected_program,
            )

    @tag("controllers.program.fetch_programs_by_program_member")
    def test_fetch_programs_by_program_member(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given `ProgramMember`'s `User` email."""

        programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
            program_ids=[],
            pa_numbers=[],
            tiers=[],
            program_member=arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_USER_EMAIL,
            page=None,
            limit=None,
        )

        self.assertIsInstance(programs, QuerySet[models.Program])

        self.assertEqual(
            programs.count(), len(arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_VALID_IDS)
        )

        for program in programs:
            self.assertIsInstance(program, models.Program)

            program_id: int = program.id

            self.assertIn(program_id, self.program_fixtures)
            self.assertIn(
                program_id, arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_VALID_IDS
            )

            serialized_program = ProgramSerializer(program).data
            expected_program = self.program_fixtures[program_id]

            del serialized_program["segment"]
            del serialized_program["created"]
            del serialized_program["modified"]

            self.assertEqual(
                serialized_program,
                expected_program,
            )

    @tag("controllers.program.fetch_programs_by_program_member_no_program_member")
    def test_fetch_programs_by_program_member_no_program_member(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given `ProgramMember`'s `User` email, where the
        `User` does not have an active `ProgramMember` entry."""

        programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
            program_ids=[],
            pa_numbers=[],
            tiers=[],
            program_member=arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_NO_ACTIVE_PROGRAM_MEMBER_USER_EMAIL,
            page=None,
            limit=None,
        )

        self.assertIsInstance(programs, QuerySet[models.Program])

        self.assertEqual(
            programs.count(),
            arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_NO_ACTIVE_PROGRAM_MEMBER_PROGRAM_COUNT,
        )

    @tag("controllers.program.fetch_programs_by_tiers_and_program_member")
    def test_fetch_programs_by_tiers_and_program_member(self) -> None:
        """Success Case: Fetch active `Program` records for
        the given tiers and `ProgramMember`'s `User` email."""

        programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
            program_ids=[],
            pa_numbers=[],
            tiers=arguments.FETCH_PROGRAMS_BY_TIERS_AND_PROGRAM_MEMBER_TIERS,
            program_member=arguments.FETCH_PROGRAMS_BY_PROGRAM_MEMBER_USER_EMAIL,
            page=None,
            limit=None,
        )

        self.assertIsInstance(programs, QuerySet[models.Program])

        self.assertEqual(
            programs.count(),
            len(arguments.FETCH_PROGRAMS_BY_TIERS_AND_PROGRAM_MEMBER_VALID_IDS),
        )

        for program in programs:
            self.assertIsInstance(program, models.Program)

            program_id: int = program.id

            self.assertIn(program_id, self.program_fixtures)
            self.assertIn(
                program_id,
                arguments.FETCH_PROGRAMS_BY_TIERS_AND_PROGRAM_MEMBER_VALID_IDS,
            )

            serialized_program = ProgramSerializer(program).data
            expected_program = self.program_fixtures[program_id]

            del serialized_program["segment"]
            del serialized_program["created"]
            del serialized_program["modified"]

            self.assertEqual(
                serialized_program,
                expected_program,
            )

    @tag("controllers.program.fetch_programs_with_page")
    def test_fetch_programs_with_page(self) -> None:
        """Success Case: Fetch page of active `Program` records."""

        programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
            program_ids=[],
            pa_numbers=[],
            tiers=[],
            program_member="",
            page=arguments.FETCH_PROGRAM_WITH_PAGE,
            limit=None,
        )

        self.assertIsInstance(programs, QuerySet[models.Program])

        self.assertEqual(
            programs.count(),
            arguments.FETCH_PROGRAM_WITH_PAGE_EXPECTED_COUNT,
        )

        for program in programs:
            self.assertIsInstance(program, models.Program)

            program_id: int = program.id

            self.assertIn(program_id, self.program_fixtures)

            serialized_program = ProgramSerializer(program).data
            expected_program = self.program_fixtures[program_id]

            del serialized_program["segment"]
            del serialized_program["created"]
            del serialized_program["modified"]

            self.assertEqual(
                serialized_program,
                expected_program,
            )

    @tag("controllers.program.fetch_programs_with_limit")
    def test_fetch_programs_with_limit(self) -> None:
        """Success Case: Fetch active `Program` records up to a limit."""

        programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
            program_ids=[],
            pa_numbers=[],
            tiers=[],
            program_member="",
            page=None,
            limit=arguments.FETCH_PROGRAM_WITH_LIMIT,
        )

        self.assertIsInstance(programs, QuerySet[models.Program])

        self.assertEqual(programs.count(), arguments.FETCH_PROGRAM_WITH_LIMIT)

    @tag("controllers.program.fetch_programs_with_page_and_limit")
    def test_fetch_programs_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of active `Program` records up to a limit."""

        programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
            program_ids=[],
            pa_numbers=[],
            tiers=[],
            program_member="",
            page=arguments.FETCH_PROGRAM_WITH_PAGE,
            limit=arguments.FETCH_PROGRAM_WITH_LIMIT,
        )

        self.assertIsInstance(programs, QuerySet[models.Program])

        self.assertEqual(
            programs.count(), len(arguments.FETCH_PROGRAM_WITH_PAGE_AND_LIMIT_VALID_IDS)
        )

        for program in programs:
            self.assertIsInstance(program, models.Program)

            program_id: int = program.id

            self.assertIn(program_id, self.program_fixtures)

            serialized_program = ProgramSerializer(program).data
            expected_program = self.program_fixtures[program_id]

            del serialized_program["segment"]
            del serialized_program["created"]
            del serialized_program["modified"]

            self.assertEqual(
                serialized_program,
                expected_program,
            )

    @tag("controllers.program.fetch_programs_with_page_exceeding_max_page")
    def test_fetch_programs_with_page_exceeding_max_page(self) -> None:
        """Success Case: Fetch active `Program` records using a
        page number that exceeds the number of pages."""

        programs = controllers.Program.fetch_programs(  # type: ignore[attr-defined]
            program_ids=[],
            pa_numbers=[],
            tiers=[],
            program_member="",
            page=arguments.FETCH_PROGRAM_WITH_PAGE_EXCEEDING_MAX_PAGE_COUNT,
            limit=None,
        )

        self.assertIsInstance(programs, QuerySet[models.Program])
        self.assertEqual(
            programs.count(),
            arguments.FETCH_PROGRAM_WITH_PAGE_EXCEEDING_MAX_PAGE_COUNT_RECORD_COUNT,
        )

    @tag("controllers.program.fetch_programs_by_ids_and_pa_numbers")
    def test_fetch_programs_by_ids_and_pa_numbers(self) -> None:
        """Fail Case: Fetch `Program` records for
        by both ids and PA numbers."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Program.fetch_programs(  # type: ignore[attr-defined]
                program_ids=arguments.FETCH_PROGRAM_IDS,
                pa_numbers=arguments.FETCH_PROGRAM_PA_NUMBERS,
                tiers=[],
                program_member="",
                page=None,
                limit=None,
            )

    @tag("controllers.program.fetch_programs_ids_dne")
    def test_fetch_programs_ids_dne(self) -> None:
        """Fail Case: Fetch `Program` records for
        ids that do not exist."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Program.fetch_programs(  # type: ignore[attr-defined]
                program_ids=arguments.FETCH_PROGRAM_BY_PROGRAM_ID_DNE,
                pa_numbers=[],
                tiers=[],
                program_member="",
                page=None,
                limit=None,
            )

    @tag("controllers.program.fetch_programs_pa_numbers_dne")
    def test_fetch_programs_pa_numbers_dne(self) -> None:
        """Fail Case: Fetch `Program` records for
        PA numbers that do not exist."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Program.fetch_programs(  # type: ignore[attr-defined]
                program_ids=[],
                pa_numbers=arguments.FETCH_PROGRAM_BY_PROGRAM_PA_NUMBER_DNE,
                tiers=[],
                program_member="",
                page=None,
                limit=None,
            )

    @tag("controllers.program.fetch_programs_program_member_user_dne")
    def test_fetch_programs_program_member_user_dne(self) -> None:
        """Fail Case: Fetch `Program` records for
        a `ProgramMember` `User` that does not exist."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Program.fetch_programs(  # type: ignore[attr-defined]
                program_ids=[],
                pa_numbers=[],
                tiers=[],
                program_member=arguments.FETCH_PROGRAMS_PROGRAM_MEMBER_USER_DNE_EMAIL,
                page=None,
                limit=None,
            )
