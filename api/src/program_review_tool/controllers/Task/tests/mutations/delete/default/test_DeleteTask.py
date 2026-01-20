"""
Collection of pytests for Task's delete controller.
"""

import pytest
from typing import cast, List

# pylint: disable=line-too-long
from django.contrib.auth import models as AuthModels
from django.test import tag

from program_review_tool import controllers, exceptions
from program_review_tool.controllers.Task.tests.mutations.delete.default import (
    arguments,
)

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "task",
    "program_review_tool",
    "controllers.TestDeleteTask",
    "task.delete.default",
    "program_review_tool.task.delete",
)
class TestDeleteTask(MultiDBTestCase):
    """Test suite for Task's delete controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/programs.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/program_members.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/tasks.json",
    ]

    @tag("controllers.task.delete_task")
    def test_delete_task(self) -> None:
        """Success Case: Delete `Task` record with the given id."""

        user = AuthModels.User.objects.get(username=arguments.DELETE_TASK_USER_EMAIL)
        rows_affected = controllers.Task.delete_task(
            task_id=arguments.DELETE_TASK_TASK_ID,
            user=user,
            reporting_period=arguments.DELETE_TASK_REPORTING_PERIOD,
        )
        self.assertEqual(rows_affected, arguments.EXPECTED_ROWS_AFFECTED)

    @tag("controllers.task.delete_task_user_not_authenticated")
    def test_delete_task_user_not_authenticated(self) -> None:
        """Fail Case: Delete `Task` record for a `User`
        that is not authenticated."""

        user = cast(AuthModels.User, AuthModels.AnonymousUser())
        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.delete_task(
                task_id=arguments.DELETE_TASK_TASK_ID,
                user=user,
                reporting_period=arguments.DELETE_TASK_REPORTING_PERIOD,
            )

    @tag("controllers.task.delete_task_multiple_reporting_periods")
    def test_delete_task_multiple_reporting_periods(self) -> None:
        """Fail Case: Delete `Task` record with multiple reporting periods."""

        user = AuthModels.User.objects.get(username=arguments.DELETE_TASK_USER_EMAIL)
        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.delete_task(
                task_id=arguments.DELETE_TASK_TASK_ID_MULTIPLE_REPORTING_PERIODS,
                user=user,
                reporting_period=arguments.DELETE_TASK_REPORTING_PERIOD,
            )

    @tag("controllers.task.delete_task_wrong_reporting_period")
    def test_delete_task_wrong_reporting_period(self) -> None:
        """Fail Case: Delete `Task` record with wrong reporting period."""

        user = AuthModels.User.objects.get(username=arguments.DELETE_TASK_USER_EMAIL)
        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.delete_task(
                task_id=arguments.DELETE_TASK_TASK_ID,
                user=user,
                reporting_period=arguments.DELETE_TASK_REPORTING_PERIOD_WRONG_REPORTING_PERIOD,
            )
