"""
Collection of pytests for Task's fetch controller.
"""

from typing import List

from django.db.models import QuerySet
from django.test import tag

from program_review_tool import controllers, models
from program_review_tool.controllers.Task.tests.query.read.default import arguments
from program_review_tool.models.Task.serializers import TaskSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "task",
    "program_review_tool",
    "controllers.TestFetchTask",
    "task.fetch.default",
    "program_review_tool.task.fetch",
)
class TestFetchTask(MultiDBTestCase):
    """Test suite for Task's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/programs.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/program_members.json",
        "program_review_tool/controllers/Task/tests/query/read/default/fixtures/tasks.json",
    ]

    @tag("controllers.task.fetch_previous_tasks")
    def test_fetch_previous_tasks(self) -> None:
        """Success Case: Fetch `Task` records for
        a previous reporting period."""

        # Fetch tasks.
        tasks = controllers.Task.fetch_tasks(
            pa_number=arguments.FETCH_TASKS_PA_NUMBER,
            reporting_period=arguments.FETCH_TASKS_PREVIOUS_PERIOD,
        )

        # Ensure data is a `Task` queryset.
        self.assertIsInstance(tasks, QuerySet[models.Task])

        data = list(TaskSerializer(tasks, many=True).data)

        # Ensure the data is correct.
        self.assertEqual(data, arguments.FETCH_TASKS_PREVIOUS_EXPECTED_TASKS)

    @tag("controllers.task.fetch_current_tasks")
    def test_fetch_current_tasks(self) -> None:
        """Success Case: Fetch `Task` records for
        a current reporting period."""

        # Fetch tasks.
        tasks = controllers.Task.fetch_tasks(
            pa_number=arguments.FETCH_TASKS_PA_NUMBER,
            reporting_period=arguments.FETCH_TASKS_CURRENT_PERIOD,
        )

        # Ensure data is a `Task` queryset.
        self.assertIsInstance(tasks, QuerySet[models.Task])

        data = list(TaskSerializer(tasks, many=True).data)

        # Ensure the data is correct.
        self.assertEqual(data, arguments.FETCH_TASKS_CURRENT_EXPECTED_TASKS)

    @tag("controllers.task.fetch_future_tasks")
    def test_fetch_future_tasks(self) -> None:
        """Success Case: Fetch `Task` records for
        a future reporting period."""

        # Fetch tasks.
        tasks = controllers.Task.fetch_tasks(
            pa_number=arguments.FETCH_TASKS_PA_NUMBER,
            reporting_period=arguments.FETCH_TASKS_FUTURE_PERIOD,
        )

        # Ensure data is a `Task` queryset.
        self.assertIsInstance(tasks, QuerySet[models.Task])

        data = list(TaskSerializer(tasks, many=True).data)

        # Ensure the data is correct.
        self.assertEqual(data, [])

    @tag("controllers.task.fetch_empty_tasks")
    def test_fetch_empty_tasks(self) -> None:
        """Success Case: Fetch `Task` records for
        an empty PA Number with a current reporting period."""

        # Fetch tasks.
        tasks = controllers.Task.fetch_tasks(
            pa_number=arguments.FETCH_TASKS_EMPTY_PA_NUMBER,
            reporting_period=arguments.FETCH_TASKS_CURRENT_PERIOD,
        )

        # Ensure data is a `Task` queryset.
        self.assertIsInstance(tasks, QuerySet[models.Task])

        data = list(TaskSerializer(tasks, many=True).data)

        # Ensure the data is correct.
        self.assertEqual(data, [])
