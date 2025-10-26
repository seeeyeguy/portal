"""
Collection of pytests for Resource's update controller.
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
    "controllers.TestUpdateTask",
    "task.update.default",
    "program_review_tool.task.update",
)
class TestUpdateTask(MultiDBTestCase):
    """Test suite for Task's update controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/programs.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/program_members.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/tasks.json",
    ]

    @tag("controllers.task.update_task")
    def test_update_task(self) -> None:
        """Success Case: Update a `Task` record."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.UPDATE_TASK_USER_EMAIL)

        # Update task for the user.
        task, rows_affected = controllers.Task.update_task(
            task_id=arguments.UPDATE_TASK_TASK_ID,
            user=user,
            pa_number=arguments.UPDATE_TASK_PA_NUMBER,
            reporting_period=arguments.UPDATE_TASK_REPORTING_PERIOD,
            name=arguments.UPDATE_TASK_NAME,
            description=arguments.UPDATE_TASK_DESCRIPTION,
            owner=arguments.UPDATE_TASK_OWNER_EMAIL,
            status=arguments.UPDATE_TASK_STATUS,
            order=arguments.UPDATE_TASK_ORDER,
            target_date=arguments.UPDATE_TASK_TARGET_DATE,
            complete_date=arguments.UPDATE_TASK_COMPLETE_DATE,
            archive_date=arguments.UPDATE_TASK_ARCHIVE_DATE,
        )

        # Ensure data is a `Task` instance.
        self.assertIsInstance(task, models.Task)

        self.assertEqual(rows_affected, arguments.UPDATE_TASK_EXPECTED_ROWS_AFFECTED)

        data: dict = TaskSerializer(task).data

        # Ensure data is correct.
        self.assertDictEqual(data, arguments.UPDATE_TASK_EXPECTED_RESPONSE)

    @tag("controllers.task.update_task_user_not_authenticated")
    def test_update_task_user_not_authenticated(self) -> None:
        """Fail Case: Update a `Task` record with a `User`
        that is not authenticated."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.update_task(
                task_id=arguments.UPDATE_TASK_TASK_ID,
                user=cast(AuthModels.User, AuthModels.AnonymousUser()),
                pa_number=arguments.UPDATE_TASK_PA_NUMBER,
                reporting_period=arguments.UPDATE_TASK_REPORTING_PERIOD,
                name=arguments.UPDATE_TASK_NAME,
                description=arguments.UPDATE_TASK_DESCRIPTION,
                owner=arguments.UPDATE_TASK_OWNER_EMAIL,
                status=arguments.UPDATE_TASK_STATUS,
                order=arguments.UPDATE_TASK_ORDER,
                target_date=arguments.UPDATE_TASK_TARGET_DATE,
                complete_date=arguments.UPDATE_TASK_COMPLETE_DATE,
                archive_date=arguments.UPDATE_TASK_ARCHIVE_DATE,
            )

    @tag("controllers.task.update_task_task_dne")
    def test_update_task_task_dne(self) -> None:
        """Fail Case: Update a `Task` record that
        does not exist."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.UPDATE_TASK_USER_EMAIL)

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.update_task(
                task_id=arguments.UPDATE_TASK_TASK_ID_DNE,
                user=user,
                pa_number=arguments.UPDATE_TASK_PA_NUMBER,
                reporting_period=arguments.UPDATE_TASK_REPORTING_PERIOD,
                name=arguments.UPDATE_TASK_NAME,
                description=arguments.UPDATE_TASK_DESCRIPTION,
                owner=arguments.UPDATE_TASK_OWNER_EMAIL,
                status=arguments.UPDATE_TASK_STATUS,
                order=arguments.UPDATE_TASK_ORDER,
                target_date=arguments.UPDATE_TASK_TARGET_DATE,
                complete_date=arguments.UPDATE_TASK_COMPLETE_DATE,
                archive_date=arguments.UPDATE_TASK_ARCHIVE_DATE,
            )

    @tag("controllers.task.update_task_multiple_reporting_periods")
    def test_update_task_multiple_reporting_periods(self) -> None:
        """Fail Case: Update a `Task` record that
        exists across multiple reporting periods."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.UPDATE_TASK_USER_EMAIL)

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.update_task(
                task_id=arguments.UPDATE_TASK_TASK_ID_MULTIPLE_REPORTING_PERIODS,
                user=user,
                pa_number=arguments.UPDATE_TASK_PA_NUMBER,
                reporting_period=arguments.UPDATE_TASK_REPORTING_PERIOD,
                name=arguments.UPDATE_TASK_NAME,
                description=arguments.UPDATE_TASK_DESCRIPTION,
                owner=arguments.UPDATE_TASK_OWNER_EMAIL,
                status=arguments.UPDATE_TASK_STATUS,
                order=arguments.UPDATE_TASK_ORDER,
                target_date=arguments.UPDATE_TASK_TARGET_DATE,
                complete_date=arguments.UPDATE_TASK_COMPLETE_DATE,
                archive_date=arguments.UPDATE_TASK_ARCHIVE_DATE,
            )

    @tag("controllers.task.update_task_wrong_pa_number")
    def test_update_task_wrong_pa_number(self) -> None:
        """Fail Case: Update a `Task` record that
        using the wrong PA number."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.UPDATE_TASK_USER_EMAIL)

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.update_task(
                task_id=arguments.UPDATE_TASK_TASK_ID,
                user=user,
                pa_number=arguments.UPDATE_TASK_PA_NUMBER_WRONG_PA_NUMBER,
                reporting_period=arguments.UPDATE_TASK_REPORTING_PERIOD,
                name=arguments.UPDATE_TASK_NAME,
                description=arguments.UPDATE_TASK_DESCRIPTION,
                owner=arguments.UPDATE_TASK_OWNER_EMAIL,
                status=arguments.UPDATE_TASK_STATUS,
                order=arguments.UPDATE_TASK_ORDER,
                target_date=arguments.UPDATE_TASK_TARGET_DATE,
                complete_date=arguments.UPDATE_TASK_COMPLETE_DATE,
                archive_date=arguments.UPDATE_TASK_ARCHIVE_DATE,
            )

    @tag("controllers.task.update_task_wrong_reporting_period")
    def test_update_task_wrong_reporting_period(self) -> None:
        """Fail Case: Update a `Task` record that
        using the wrong reporting period."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.UPDATE_TASK_USER_EMAIL)

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.update_task(
                task_id=arguments.UPDATE_TASK_TASK_ID,
                user=user,
                pa_number=arguments.UPDATE_TASK_PA_NUMBER,
                reporting_period=arguments.UPDATE_TASK_REPORTING_PERIOD_WRONG_REPORTING_PERIOD,
                name=arguments.UPDATE_TASK_NAME,
                description=arguments.UPDATE_TASK_DESCRIPTION,
                owner=arguments.UPDATE_TASK_OWNER_EMAIL,
                status=arguments.UPDATE_TASK_STATUS,
                order=arguments.UPDATE_TASK_ORDER,
                target_date=arguments.UPDATE_TASK_TARGET_DATE,
                complete_date=arguments.UPDATE_TASK_COMPLETE_DATE,
                archive_date=arguments.UPDATE_TASK_ARCHIVE_DATE,
            )
