"""
Collection of pytests for Request's create view endpoint.
"""

import json
from typing import List

from django.contrib.auth import models as AuthModels
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import tag
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from request import models
from request.controllers.Request.tests.mutations.create.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "request_app",
    "request",
    "views",
    "request_app.request.create",
    "request.create.default",
    "views.TestCreateRequest",
)
class TestCreateRequest(MultiDBTestCase):
    """
    Tests for POST /v1/request/request endpoint.
    """

    @override_settings(
        STORAGES={"default": {"BACKEND": "django.core.files.storage.InMemoryStorage"}}
    )
    def setUp(self) -> None:

        super().setUp()

        self.client = APIClient()

        user = AuthModels.User.objects.get(username=arguments.CREATE_REQUEST_USER_EMAIL)
        self.client.force_login(user=user)

        # Create a standard set of params.
        self.params = {
            k: v
            for k, v in arguments.BASE_CREATE_REQUEST_STRUCTURE_PARAMS.copy().items()
            if v is not None and k != "originator"
        }

        self.params["employee_levels"] = json.dumps(self.params["employee_levels"])
        self.params["subfunctions"] = json.dumps(self.params["subfunctions"])
        self.params["tags"] = json.dumps(self.params["tags"])
        self.params["point_of_contacts"] = json.dumps(self.params["point_of_contacts"])

        self.params["thumbnail"] = SimpleUploadedFile(
            name="thumbnail.png",
            content=open(
                "manager/storage/static/lhx/images/icons/l3harrislogo.png", "rb+"
            ).read(),
            content_type="image/png",
        )

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "request/controllers/Request/tests/mutations/create/default/fixtures/users.json",
    ]

    url: str = reverse("request.request")

    @tag("views.request.create_request")
    @override_settings(
        STORAGES={"default": {"BACKEND": "django.core.files.storage.InMemoryStorage"}}
    )
    def test_create_request(self) -> None:
        """Success Case: Create a `Request` record."""

        response = self.client.post(
            self.url,
            data=self.params,
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertIsInstance(data, dict)

        del data["id"]
        del data["created"]
        del data["modified"]

        del data["resource"]["id"]
        del data["resource"]["uid"]
        del data["resource"]["thumbnail"]
        del data["resource"]["created"]

        transitions: dict = data.pop("transitions", {})

        self.assertDictEqual(data, arguments.VALID_CREATED_REQUEST_DRAFT)

        stages = [models.Stage.StageLevels.DRAFT]
        nodes = transitions["nodes"].items()
        for i, item in enumerate(nodes):
            self.assertEqual(item[1]["stage"]["level"], stages[i])

    @tag("views.request.create_request_submitted")
    @override_settings(
        STORAGES={"default": {"BACKEND": "django.core.files.storage.InMemoryStorage"}}
    )
    def test_create_request_submitted(self) -> None:
        """Success Case: Create and submit a `Request` record."""

        params = self.params.copy()
        params["stage"] = "SUBMITTED"

        response = self.client.post(
            self.url,
            data=params,
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()

        self.assertIsInstance(data, dict)

        del data["id"]
        del data["created"]
        del data["modified"]

        del data["resource"]["id"]
        del data["resource"]["uid"]
        del data["resource"]["thumbnail"]
        del data["resource"]["created"]

        transitions: dict = data.pop("transitions", {})

        self.assertDictEqual(data, arguments.VALID_CREATED_REQUEST_SUBMITTED)

        stages = [models.Stage.StageLevels.SUBMITTED, models.Stage.StageLevels.DRAFT]
        nodes = transitions["nodes"].items()
        for i, item in enumerate(nodes):
            self.assertEqual(item[1]["stage"]["level"], stages[i])

    @tag("views.request.create_request_user_permissions_denied")
    def test_create_request_user_permissions_denied(self) -> None:
        """Fail Case: Create a `Request` record with a `User` that
        does not have the appropriate permissions."""

        user = AuthModels.User.objects.get(
            username=arguments.CREATE_REQUEST_USER_EMAIL_INVALID_ROLE
        )
        self.client.force_login(user=user)

        response = self.client.post(
            self.url,
            data=self.params,
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @tag("views.request.create_request_stage_invalid")
    def test_create_request_stage_invalid(self) -> None:
        """Fail Case: Create a `Request` record with an
        invalid level for stage."""

        params = self.params.copy()
        params["stage"] = "INVALID"

        response = self.client.post(
            self.url,
            data=params,
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
