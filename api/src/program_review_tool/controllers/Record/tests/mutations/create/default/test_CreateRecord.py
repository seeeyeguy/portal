"""
Collection of pytests for Record's create controller.
"""

# pylint: disable=wrong-import-order
import pytest
from typing import cast, List

from django.contrib.auth import models as AuthModels
from django.test import tag

from program_review_tool import controllers, exceptions, models
from program_review_tool.controllers.Record.Record import TaskPayload
from program_review_tool.controllers.Record.tests.mutations.create.default import (
    arguments,
)

from program_review_tool.models.Record.serializers import RecordSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "program_review_tool",
    "record",
    "controllers.TestCreateRecord",
    "program_review_tool.record.create",
    "record.create.default",
)
class TestCreateRecord(MultiDBTestCase):
    """Test suite for Record's create controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Record/tests/mutations/create/default/fixtures/programs.json",
        "program_review_tool/controllers/Record/tests/mutations/create/default/fixtures/program_members.json",
        "program_review_tool/controllers/Record/tests/mutations/create/default/fixtures/records.json",
        "program_review_tool/controllers/Record/tests/mutations/create/default/fixtures/tasks.json",
    ]

    @tag("controllers.record.create_record")
    def test_create_record(self) -> None:
        """Success Case: Create a `Record` record."""

        # Query `User` from database.
        user = AuthModels.User.objects.get(username=arguments.CREATE_RECORD_USER_EMAIL)

        # Create `Record` for generation.
        record = controllers.Record.create_record(
            **arguments.CREATE_RECORD_PARAMS,
            user=user,
            pa_number=arguments.CREATE_RECORD_PROGRAM_PA_NUMBER,
            tasks=cast(List[TaskPayload], arguments.CREATE_RECORD_TASK_PARAMS),
        )

        # Ensure data is a `Record` instance.
        self.assertIsInstance(record, models.Record)

        tasks = record.tasks  # type: ignore[attr-defined]

        data: dict = RecordSerializer(record).data

        data["tasks"] = tasks
        del data["created"]
        del data["id"]
        del data["user"]
        del data["program"]

        for obj in data["team_members"]:
            obj.get("role", {}).pop("created", None)
            obj.get("role", {}).pop("modified", None)

        # Ensure data is correct.
        self.assertDictEqual(data, arguments.CREATE_RECORD_EXPECTED_RECORD)

    @tag("controllers.record.create_record_previous_revision")
    def test_create_record_previous_revision(self) -> None:
        """Success Case: Create a `Record` record with a previous revision."""

        # Query `User` from database.
        user = AuthModels.User.objects.get(username=arguments.CREATE_RECORD_USER_EMAIL)

        params: dict = {
            **arguments.CREATE_RECORD_PARAMS,
            "pa_number": arguments.CREATE_RECORD_PROGRAM_PA_NUMBER_PREVIOUS_REVISION,
            "name": arguments.CREATE_RECORD_PROGRAM_NAME_PREVIOUS_REVISION,
        }

        # Create `Record` for generation.
        record = controllers.Record.create_record(
            **params,
            user=user,
            tasks=cast(
                List[TaskPayload], arguments.CREATE_RECORD_TASK_PREVIOUS_REVISION_PARAMS
            ),
        )

        # Ensure data is a `Record` instance.
        self.assertIsInstance(record, models.Record)

        tasks = record.tasks  # type: ignore[attr-defined]

        data: dict = RecordSerializer(record).data

        data["tasks"] = tasks
        del data["created"]
        del data["id"]
        del data["user"]
        del data["program"]

        for obj in data["team_members"]:
            obj.get("role", {}).pop("created", None)
            obj.get("role", {}).pop("modified", None)

        # Ensure data is correct.
        self.assertDictEqual(
            data, arguments.CREATE_RECORD_EXPECTED_RECORD_PREVIOUS_REVISION
        )

    @tag("controllers.record.create_record_user_not_authenticated")
    def test_create_record_user_not_authenticated(self) -> None:
        """Fail Case: Create a `Record` record with a `User`
        that is not authenticated."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            # Create `Record` for generation.
            controllers.Record.create_record(
                **arguments.CREATE_RECORD_PARAMS,
                user=cast(AuthModels.User, AuthModels.AnonymousUser()),
                pa_number=arguments.CREATE_RECORD_PROGRAM_PA_NUMBER,
            )

    @tag("controllers.record.create_record_user_not_authorized")
    def test_create_record_user_not_authorized(self) -> None:
        """Fail Case: Create a `Record` record with a `User`
        that is not a program team member."""

        # Query `User` from database.
        user = AuthModels.User.objects.get(
            username=arguments.CREATE_RECORD_USER_EMAIL_UNAUTHORIZED
        )

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Record.create_record(
                **arguments.CREATE_RECORD_PARAMS,
                user=user,
                pa_number=arguments.CREATE_RECORD_PROGRAM_PA_NUMBER,
            )

    @tag("controllers.record.create_record_program_dne")
    def test_create_record_program_dne(self) -> None:
        """Fail Case: Create a `Record` record with a `Program`
        that does not exist."""

        # Query `User` from database.
        user = AuthModels.User.objects.get(username=arguments.CREATE_RECORD_USER_EMAIL)

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Record.create_record(
                **arguments.CREATE_RECORD_PARAMS,
                user=user,
                pa_number=arguments.CREATE_RECORD_PROGRAM_PA_NUMBER_DNE,
            )
