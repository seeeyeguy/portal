"""
`Program Review Tool` `Task` controller module. Controllers utilize the
Django ORM to create, fetch, update, and delete records within
the `Task` table.
"""

import logging
import datetime
from typing import Tuple, Union
from uuid import uuid4

from django.contrib.auth import models as AuthModels
from django.db.models import QuerySet

from program_review_tool import exceptions, models

from program_review_tool.utils.verify_user import verify_user

LOGGER = logging.getLogger(__name__)


class Task:
    """
    Container class for functions related to creating, updating,
    retrieving, and deleting `Task` records.
    """

    # pylint: disable=line-too-long
    @staticmethod
    def create_task(
        user: AuthModels.User,
        pa_number: str,
        reporting_period: int,
        name: str,
        owner: str,
        create_date: datetime.date,
        target_date: datetime.date,
        previous_id: Union[int, None] = None,
        order: Union[int, None] = None,
        description: str = "",
        status: str = "",
        complete_date: Union[datetime.date, None] = None,
        archive_date: Union[datetime.date, None] = None,
    ) -> models.Task:
        """
        Create a new`task` record.

        Accepts:
            * user (AuthModels.User): Authenticated user creating the task.
            * previous_id (int | None): ID of the previous revision of this task
                from the last modified reporting period.
            * pa_number (str): PA number of related `Program` for the `Task`.
            * reporting_period (int): Reporting period code (e.g. 202306 for June 2023).
            * order (int | None, optional): Display order for the task; No order for archived tasks.
            * name (str): Name of the `Task`.
            * description (str): Detailed description of the `Task`.
            * owner (AuthModels.User): User responsible for completing the task.
            * status (str): Current status description of `Task` state.
            * create_date (date): Date the task was originally created ie (first revision).
            * target_date (date): Desired completion date for the task.
            * complete_date (date | None): Actual completion date.
            * archive_date (date | None): Date the task was archived.

        Returns:
            * Task (models.Task): The newly created `Task`
                record.
        """
        try:

            LOGGER.info(
                (
                    f"Creating Task with name: {name} and program: {pa_number}"
                    f" in reporting period: {reporting_period} with previous_id: {previous_id}"
                    f" for user: {user.email if user.is_authenticated else 'None'}."
                )
            )

            if not (user and user.is_authenticated):
                raise exceptions.ProgramReviewToolError(
                    "Authentication required.", status=401
                )

            # Fetch the associated `Program` instance.
            program_record = models.Program.objects.get(pa_number=pa_number)

            previous_revision: Union[models.Task, None] = (
                models.Task.objects.get(id=previous_id) if previous_id else None
            )

            task_data = {
                "previous_revision": previous_revision,
                "program": program_record,
                "pa_number": pa_number,
                "reporting_period": [reporting_period],  # ArrayField expects a list
                "order": order,
                "name": str(uuid4()),
                "task_name": name,
                "description": description,
                "owner": verify_user(owner),
                "status": status,
                "create_date": create_date,
                "target_date": target_date,
                "complete_date": complete_date,
                "archive_date": archive_date,
            }

            task: models.Task = models.Task.objects.create(**task_data)

            return task

        except models.Program.DoesNotExist as exc:
            err_msg = f"Program (pa_number={pa_number}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404) from exc
        except models.Task.DoesNotExist as exc:
            # Raised only when previous_id is provided but not found.
            err_msg = f"Previous Task (id={previous_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404) from exc

    @staticmethod
    def update_task(
        task_id: int,
        user: AuthModels.User,
        pa_number: str,
        reporting_period: int,
        name: str,
        owner: str,
        target_date: datetime.date,
        order: Union[int, None] = None,
        description: str = "",
        status: str = "",
        complete_date: Union[datetime.date, None] = None,
        archive_date: Union[datetime.date, None] = None,
    ) -> Tuple[models.Task, int]:
        """
        Update a `Task` record for the given id with the given params.
        Only tasks that exist for a single reporting period can be updated.

        Accepts:
            * id (int): ID of the `Task` to update.
            * user (AuthModels.User): Authenticated user performing the update.
            * pa_number (str): PA number of related `Program` for the `Task`.
            * reporting_period (int): Reporting period code (e.g. 202306 for June 2023).
            * order (int | None, optional): Display order for the task; No order for archived tasks.
            * name (str): Name of the `Task`.
            * description (str): Detailed description of the `Task`.
            * owner (AuthModels.User): User responsible for completing the task.
            * status (str): Current status description of `Task` state.
            * target_date (date): Desired completion date for the task.
            * complete_date (date | None): Actual completion date.
            * archive_date (date | None): Date the task was archived.

        Returns:
            * task (models.Task): The updated `Task` record.
            * rows_affected (int): The number of `Task` records updated.
        """

        try:
            LOGGER.info(
                (
                    f"Updating Task id: {task_id} with name: {name} and program: {pa_number} "
                    f"in reporting period: {reporting_period} "
                    f"for user: {user.email if user.is_authenticated else 'None'}."
                )
            )

            # Ensure `User` is authenticated.
            if not (user and user.is_authenticated):
                raise exceptions.ProgramReviewToolError(
                    "Authentication required.", status=401
                )

            # Fetch `Task` record by id.
            task_record: models.Task = models.Task.objects.get(
                id=task_id, pa_number=pa_number
            )

            stored_periods = task_record.reporting_period or []
            if len(stored_periods) != 1 or stored_periods[0] != reporting_period:
                raise exceptions.ProgramReviewToolError(
                    f"Task (id={task_id}) spans multiple reporting periods; "
                    f"cannot update for reporting_period={reporting_period}.",
                    status=400,
                )

            task_data = {
                "order": order,
                "task_name": name,
                "description": description,
                "owner": verify_user(owner),
                "status": status,
                "target_date": target_date,
                "complete_date": complete_date,
                "archive_date": archive_date,
            }

            # Update the `Task` record.
            rows_affected: int = models.Task.objects.filter(id=task_id).update(
                **task_data
            )

            task_record.refresh_from_db()

            return task_record, rows_affected
        except models.Task.DoesNotExist as exc:
            err_msg = f"Task (id={task_id}, pa_number={pa_number}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404) from exc

    @staticmethod
    def delete_task(task_id: int, user: AuthModels.User, reporting_period: int) -> int:
        """
        Delete the `Task` record with the given id.
        Only tasks that exist for a single reporting period can be deleted.

        Accepts:
            * id (int): The id of the `Task` record being deleted.
            * user (AuthModels.User): Authenticated user performing the delete.
            * reporting_period (int): Reporting period code (e.g. 202306 for June 2023).

        Returns:
            * rows_affected (int): Number of rows removed.
        """

        LOGGER.info(f"Deleting Task instance with id: {task_id}.")

        if not (user and user.is_authenticated):
            raise exceptions.ProgramReviewToolError(
                "Authentication required.", status=401
            )

        # Fetch `Task` record by id.
        task_record: models.Task = models.Task.objects.get(id=task_id)

        stored_periods = task_record.reporting_period or []
        if len(stored_periods) != 1 or stored_periods[0] != reporting_period:
            raise exceptions.ProgramReviewToolError(
                f"Task (id={task_id}) spans multiple reporting periods; "
                f"cannot delete for reporting_period={reporting_period}.",
                status=400,
            )

        task_record: QuerySet[models.Task] = models.Task.objects.filter(id=task_id)

        rows_affected, _ = task_record.delete()

        return rows_affected

    @staticmethod
    def add_reporting_period(
        task_id: int,
        user: AuthModels.User,
        pa_number: str,
        reporting_period: int,
    ) -> Tuple[models.Task, int]:
        """
        Append a new reporting period to the reporting_period array of a
        `Task`.  Validates that the task belongs to the supplied pa_number.

        Accepts:
            * id (int): The id of the `Task` record being deleted.
            * user (AuthModels.User): Authenticated user performing the delete.
            * pa_number (str): PA number of related `Program` for the `Task`.
            * reporting_period (int): Reporting period to be added.

        Returns:
            * task (models.Task): The updated `Task` record.
            * rows_affected (int): The number of `Task` records updated.
        """

        # Auth check
        if not (user and user.is_authenticated):
            raise exceptions.ProgramReviewToolError(
                "Authentication required.", status=401
            )

        try:
            task: models.Task = models.Task.objects.get(id=task_id)
        except models.Task.DoesNotExist as exc:
            err_msg = f"Task (id={task_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404) from exc

        if task.pa_number != pa_number:
            raise exceptions.ProgramReviewToolError(
                f"Task (id={task_id}) does not belong to pa_number={pa_number}.",
                status=400,
            )

        if task.reporting_period is None:
            task.reporting_period = []

        # Append the new period and save.
        if reporting_period not in task.reporting_period:  # type: ignore[operator]
            task.reporting_period.append(reporting_period)  # type: ignore[union-attr]
            task.save(update_fields=["reporting_period"])
            task.refresh_from_db()

        LOGGER.info(
            f"Added reporting_period: {reporting_period} to Task: {task_id} "
            f"for program: {pa_number} and user: {user.email if user.is_authenticated else 'None'}."
        )
        return task, 1

    @staticmethod
    def remove_reporting_period(
        task_id: int,
        user: AuthModels.User,
        pa_number: str,
        reporting_period: int,
    ) -> Tuple[models.Task, int]:
        """
        Remove a reporting period from the reporting_period array of a
        `Task`. Validates that the task belongs to the supplied pa_number.

        Accepts:
            * id (int): The id of the `Task` record being deleted.
            * user (AuthModels.User): Authenticated user performing the delete.
            * pa_number (str): PA number of related `Program` for the `Task`.
            * reporting_period (int): Reporting period to be removed.

        Returns:
            * task (models.Task): The updated `Task` record.
            * rows_affected (int): The number of `Task` records updated.
        """

        # Auth check
        if not (user and user.is_authenticated):
            raise exceptions.ProgramReviewToolError(
                "Authentication required.", status=401
            )

        try:
            task: models.Task = models.Task.objects.get(id=task_id)
        except models.Task.DoesNotExist as exc:
            err_msg = f"Task (id={task_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404) from exc

        if task.pa_number != pa_number:
            raise exceptions.ProgramReviewToolError(
                f"Task (id={task_id}) does not belong to pa_number={pa_number}.",
                status=400,
            )

        if task.reporting_period is None:
            task.reporting_period = []

        # Remove the period and save.
        if reporting_period in task.reporting_period:  # type: ignore[operator]
            task.reporting_period.remove(reporting_period)  # type: ignore[union-attr]
            task.save(update_fields=["reporting_period"])
            task.refresh_from_db()

        LOGGER.info(
            f"Removed reporting_period: {reporting_period} from Task: {task_id} "
            f"for program: {pa_number} and user: {user.email if user.is_authenticated else 'None'}."
        )
        return task, 1

    @staticmethod
    def fetch_tasks(pa_number: str, reporting_period: int) -> QuerySet[models.Task]:
        """
        Fetch all `Tasks` for a given pa_number that contain the specified reporting_period.

        Accepts:
            * pa_number (str): Program identifier to filter tasks.
            * reporting_period (int): Reporting period code (e.g. 202306).
                The query checks that the reporting_period array contains this value.

        Returns:
            tasks (QuerySet[models.Tasks]): All `Task` records
                for a given pa_number that contain the specified reporting_period.
        """

        tasks = models.Task.objects.filter(
            pa_number=pa_number, reporting_period__contains=[reporting_period]
        )

        return tasks
