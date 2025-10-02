"""
Collection of pytests for Resource's create controller.
"""

import pytest
from typing import cast, List

from django.contrib.auth import models as AuthModels
from django.test import tag

from program_review_tool import controllers, exceptions, models
from program_review_tool.controllers.Task.tests.mutations.create.default import (
    arguments,
)
from program_review_tool.models.Task.serializers import TaskSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "task",
    "program_review_tool",
    "controllers.TestCreateTask",
    "task.create.default",
    "program_review_tool.task.create",
)
class TestCreateTask(MultiDBTestCase):
    """Test suite for Task's create controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/programs.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/program_members.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/tasks.json",
    ]

    @tag("controllers.task.create_task")
    def test_create_task(self) -> None:
        """Success Case: Create a `Task` record."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.CREATE_TASK_USER_EMAIL)

        # Update task for the user.
        task = controllers.Task.create_task(
            user=user,
            pa_number=arguments.CREATE_TASK_PA_NUMBER,
            reporting_period=arguments.CREATE_TASK_REPORTING_PERIOD,
            name=arguments.CREATE_TASK_NAME,
            description=arguments.CREATE_TASK_DESCRIPTION,
            owner=arguments.CREATE_TASK_OWNER_EMAIL,
            status=arguments.CREATE_TASK_STATUS,
            order=arguments.CREATE_TASK_ORDER,
            create_date=arguments.CREATE_TASK_CREATE_DATE,
            target_date=arguments.CREATE_TASK_TARGET_DATE,
        )

        # Ensure data is a `Task` instance.
        self.assertIsInstance(task, models.Task)

        data: dict = TaskSerializer(task).data

        del data["program"]

        # Ensure data is correct.
        self.assertDictEqual(data, arguments.CREATE_TASK_EXPECTED_RESPONSE)

    @tag("controllers.task.create_task_previous_revision")
    def test_create_task_previous_revision(self) -> None:
        """Success Case: Create a `Task` record with a previous revision"""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.CREATE_TASK_USER_EMAIL)

        # Update task for the user.
        task = controllers.Task.create_task(
            user=user,
            pa_number=arguments.CREATE_TASK_PA_NUMBER,
            reporting_period=arguments.CREATE_TASK_REPORTING_PERIOD,
            previous_id=arguments.CREATE_TASK_PREVIOUS_REVISION,
            name=arguments.CREATE_TASK_NAME,
            description=arguments.CREATE_TASK_DESCRIPTION,
            owner=arguments.CREATE_TASK_OWNER_EMAIL,
            status=arguments.CREATE_TASK_STATUS,
            order=arguments.CREATE_TASK_ORDER,
            create_date=arguments.CREATE_TASK_CREATE_DATE,
            target_date=arguments.CREATE_TASK_TARGET_DATE,
        )

        # Ensure data is a `Task` instance.
        self.assertIsInstance(task, models.Task)

        data: dict = TaskSerializer(task).data

        del data["program"]

        # Ensure data is correct.
        self.assertDictEqual(
            data, arguments.CREATE_TASK_PREVIOUS_REVISION_EXPECTED_RESPONSE
        )

    @tag("controllers.task.create_task_user_not_authenticated")
    def test_create_task_user_not_authenticated(self) -> None:
        """Fail Case: Create a `Task` record with a `User`
        that is not authenticated."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.create_task(
                user=cast(AuthModels.User, AuthModels.AnonymousUser()),
                pa_number=arguments.CREATE_TASK_PA_NUMBER,
                reporting_period=arguments.CREATE_TASK_REPORTING_PERIOD,
                name=arguments.CREATE_TASK_NAME,
                description=arguments.CREATE_TASK_DESCRIPTION,
                owner=arguments.CREATE_TASK_OWNER_EMAIL,
                status=arguments.CREATE_TASK_STATUS,
                order=arguments.CREATE_TASK_ORDER,
                create_date=arguments.CREATE_TASK_CREATE_DATE,
                target_date=arguments.CREATE_TASK_TARGET_DATE,
            )

    @tag("controllers.task.update_task_previous_revision_dne")
    def test_update_task_previous_revision_dne(self) -> None:
        """Fail Case: Update a `Task` record with previous revision
        that does not exist."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.CREATE_TASK_USER_EMAIL)

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.create_task(
                user=user,
                pa_number=arguments.CREATE_TASK_PA_NUMBER,
                reporting_period=arguments.CREATE_TASK_REPORTING_PERIOD,
                previous_id=arguments.CREATE_TASK_PREVIOUS_REVISION_DNE,
                name=arguments.CREATE_TASK_NAME,
                description=arguments.CREATE_TASK_DESCRIPTION,
                owner=arguments.CREATE_TASK_OWNER_EMAIL,
                status=arguments.CREATE_TASK_STATUS,
                order=arguments.CREATE_TASK_ORDER,
                create_date=arguments.CREATE_TASK_CREATE_DATE,
                target_date=arguments.CREATE_TASK_TARGET_DATE,
            )

    @tag("controllers.task.update_task_pa_number_dne")
    def test_update_task_pa_number_dne(self) -> None:
        """Fail Case: Create a `Task` record with a
        PA number that does not exist."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.CREATE_TASK_USER_EMAIL)

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Task.create_task(
                user=user,
                pa_number=arguments.CREATE_TASK_PA_NUMBER_DNE,
                reporting_period=arguments.CREATE_TASK_REPORTING_PERIOD,
                name=arguments.CREATE_TASK_NAME,
                description=arguments.CREATE_TASK_DESCRIPTION,
                owner=arguments.CREATE_TASK_OWNER_EMAIL,
                status=arguments.CREATE_TASK_STATUS,
                order=arguments.CREATE_TASK_ORDER,
                create_date=arguments.CREATE_TASK_CREATE_DATE,
                target_date=arguments.CREATE_TASK_TARGET_DATE,
            )
