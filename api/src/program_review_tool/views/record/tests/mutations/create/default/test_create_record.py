"""
Collection of pytests for Record's create view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.core.serializers.json import DjangoJSONEncoder
from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.utils import json

from program_review_tool.controllers.Record.tests.mutations.create.default import (
    arguments,
)

from manager.utils.tests import MultiDBTestCase


@tag(
    "record",
    "program_review_tool",
    "views",
    "record.create.default",
    "program_review_tool.record.create",
    "views.TestCreateRecord",
)
class TestCreateRecord(MultiDBTestCase):
    """
    Tests for POST /v1/program-review-tool/record endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Record/tests/mutations/create/default/fixtures/programs.json",
        "program_review_tool/controllers/Record/tests/mutations/create/default/fixtures/program_members.json",
        "program_review_tool/controllers/Record/tests/mutations/create/default/fixtures/records.json",
        "program_review_tool/controllers/Record/tests/mutations/create/default/fixtures/tasks.json",
    ]

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(username=arguments.CREATE_RECORD_USER_EMAIL)
        self.client.force_login(user=user)

    url: str = reverse("program_review_tool.record")

    @tag("views.record.create_record")
    def test_create_record(self) -> None:
        """Success Case: Create a `Record` record."""

        body: dict = {
            **arguments.CREATE_RECORD_PARAMS,
            "pa_number": arguments.CREATE_RECORD_PROGRAM_PA_NUMBER,
            "tasks": arguments.CREATE_RECORD_TASK_PARAMS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        expected_record = json.loads(
            json.dumps(arguments.CREATE_RECORD_EXPECTED_RECORD, cls=DjangoJSONEncoder)
        )
        record = response.json()
        del record["created"]
        del record["id"]
        del record["user"]
        del record["program"]

        for obj in record["team_members"]:
            obj.get("role", {}).pop("created", None)
            obj.get("role", {}).pop("modified", None)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(record, expected_record)

    @tag("views.record.create_record_previous_revision")
    def test_create_record_previous_revision(self) -> None:
        """Success Case: Create a `Record` record with a previous revision."""

        body: dict = {
            **arguments.CREATE_RECORD_PARAMS,
            "pa_number": arguments.CREATE_RECORD_PROGRAM_PA_NUMBER_PREVIOUS_REVISION,
            "name": arguments.CREATE_RECORD_PROGRAM_NAME_PREVIOUS_REVISION,
            "tasks": arguments.CREATE_RECORD_TASK_PREVIOUS_REVISION_PARAMS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        expected_record = json.loads(
            json.dumps(
                arguments.CREATE_RECORD_EXPECTED_RECORD_PREVIOUS_REVISION,
                cls=DjangoJSONEncoder,
            )
        )
        record = response.json()
        del record["created"]
        del record["id"]
        del record["user"]
        del record["program"]

        for obj in record["team_members"]:
            obj.get("role", {}).pop("created", None)
            obj.get("role", {}).pop("modified", None)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(record, expected_record)

    @tag("views.record.create_record_program_dne")
    def test_create_record_program_dne(self) -> None:
        """Fail Case: Create a `Record` record with a `Program`
        that does not exist."""

        body: dict = {
            **arguments.CREATE_RECORD_PARAMS,
            "pa_number": arguments.CREATE_RECORD_PROGRAM_PA_NUMBER_DNE,
            "previous_revision": None,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.record.create_record_user_not_authenticated")
    def test_create_record_user_not_authenticated(self) -> None:
        """Fail Case: Create a `Record` record with a `User`
        that is not authenticated."""

        self.client.logout()

        body: dict = {
            **arguments.CREATE_RECORD_PARAMS,
            "pa_number": arguments.CREATE_RECORD_PROGRAM_PA_NUMBER,
            "previous_revision": None,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("views.record.create_record_user_not_authorized")
    def test_create_record_user_not_authorized(self) -> None:
        """Fail Case: Create a `Record` record with a `User`
        that is not a program team member."""

        user = AuthModels.User.objects.get(
            username=arguments.CREATE_RECORD_USER_EMAIL_UNAUTHORIZED
        )
        self.client.force_login(user=user)

        body: dict = {
            **arguments.CREATE_RECORD_PARAMS,
            "pa_number": arguments.CREATE_RECORD_PROGRAM_PA_NUMBER,
            "previous_revision": None,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
