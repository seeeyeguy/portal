"""
Collection of pytests for Resource's add reporting period controller.
"""

import pytest
from typing import cast, List

from django.contrib.auth import models as AuthModels
from django.test import tag

from program_review_tool import controllers, exceptions, models
from program_review_tool.controllers.Task.tests.mutations.update.default import (
    arguments,
)
from program_review_tool.models.Task.serializers import TaskSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "task",
    "program_review_tool",
    "controllers.TestAddReportingPeriodTask",
    "task.update.default",
    "program_review_tool.task.update",
)
class TestAddReportingPeriodTask(MultiDBTestCase):
    """Test suite for Task's add reporting period controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/programs.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/program_members.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/tasks.json",
    ]

    @tag("controllers.task.add_reporting_period_task")
    def test_add_reporting_period_task(self) -> None:
        """Success Case: Add a reporting period to a `Task` record."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.UPDATE_TASK_USER_EMAIL)

        # Update task for the user.
        task, rows_affected = controllers.Task.add_reporting_period(
            task_id=arguments.UPDATE_TASK_TASK_ID,
            user=user,
            pa_number=arguments.UPDATE_TASK_PA_NUMBER,
            reporting_period=arguments.ADD_REPORTING_PERIOD_PERIOD,
        )

        # Ensure data is a `Task` instance.
        self.assertIsInstance(task, models.Task)

        self.assertEqual(rows_affected, arguments.UPDATE_TASK_EXPECTED_ROWS_AFFECTED)

        data: dict = TaskSerializer(task).data

        del data["program"]

        # Ensure data is correct.
        self.assertDictEqual(data, arguments.ADD_REPORTING_PERIOD_EXPECTED_RESPONSE)

    @tag("controllers.task.add_reporting_period_task_user_not_authenticated")
    def test_add_reporting_period_task_user_not_authenticated(self) -> None:
        """Fail Case: Add a reporting period to a `Task` record with a `User`
        that is not authenticated."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.add_reporting_period(
                task_id=arguments.UPDATE_TASK_TASK_ID,
                user=cast(AuthModels.User, AuthModels.AnonymousUser()),
                pa_number=arguments.UPDATE_TASK_PA_NUMBER,
                reporting_period=arguments.ADD_REPORTING_PERIOD_PERIOD,
            )

    @tag("controllers.task.add_reporting_period_task_task_dne")
    def test_add_reporting_period_task_task_dne(self) -> None:
        """Fail Case: Add a reporting period to a `Task` record that
        does not exist."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.UPDATE_TASK_USER_EMAIL)

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.add_reporting_period(
                task_id=arguments.UPDATE_TASK_TASK_ID_DNE,
                user=user,
                pa_number=arguments.UPDATE_TASK_PA_NUMBER,
                reporting_period=arguments.ADD_REPORTING_PERIOD_PERIOD,
            )

    @tag("controllers.task.add_reporting_period_task_wrong_pa_number")
    def test_add_reporting_period_task_wrong_pa_number(self) -> None:
        """Fail Case: Add a reporting period to a `Task` record that
        using the wrong PA number."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.UPDATE_TASK_USER_EMAIL)

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.add_reporting_period(
                task_id=arguments.UPDATE_TASK_TASK_ID,
                user=user,
                pa_number=arguments.UPDATE_TASK_PA_NUMBER_WRONG_PA_NUMBER,
                reporting_period=arguments.ADD_REPORTING_PERIOD_PERIOD,
            )
