"""
Collection of pytests for Request's create controller.
"""

import pytest
from typing import cast, List

from django.contrib.auth import models as AuthModels
from django.test import tag

from directory import models as DirectoryModels
from request import controllers, exceptions, models
from request.controllers.Request.tests.mutations.create.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "request_app",
    "request",
    "controllers.TestCreateRequest",
    "request_app.request.create",
    "request.create.default",
)
class TestCreateRequest(MultiDBTestCase):
    """Test suite for Request's create controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "request/controllers/Request/tests/mutations/create/default/fixtures/users.json",
    ]

    @tag("controllers.request.create_request")
    def test_create_request(self) -> None:
        """Success Case: Create a `Request` record."""

        originator = AuthModels.User.objects.get(
            username=arguments.BASE_CREATE_REQUEST_STRUCTURE_PARAMS["originator"]
        )
        request = controllers.Request.create_request(
            {
                **arguments.BASE_CREATE_REQUEST_STRUCTURE_PARAMS,
                "originator": originator,
                "user": originator,
            }
        )
        self.assertIsInstance(request, models.Request)
        self.assertTrue(request.resource)
        self.assertIsInstance(request.resource, DirectoryModels.Resource)
        self.assertFalse(request.resource.active)
        self.assertEqual(request.originator.user, originator)
        self.assertEqual(request.status, models.Request.RequestStatus.PENDING)
        latest_transition = cast(
            models.Transition, request.transitions.order_by("-created").first()
        )
        self.assertEqual(
            latest_transition.stage.level,
            models.Stage.StageLevels.DRAFT,
        )

    @tag("controllers.request.create_request_submitted")
    def test_create_request_submitted(self) -> None:
        """Success Case: Create and submit a `Request` record."""

        originator = AuthModels.User.objects.get(
            username=arguments.BASE_CREATE_REQUEST_STRUCTURE_PARAMS["originator"]
        )
        request = controllers.Request.create_request(
            {
                **arguments.BASE_CREATE_REQUEST_STRUCTURE_PARAMS,
                "originator": originator,
                "user": originator,
                "stage": "SUBMITTED",
            }
        )

        self.assertIsInstance(request, models.Request)
        self.assertTrue(request.resource)
        self.assertIsInstance(request.resource, DirectoryModels.Resource)
        self.assertFalse(request.resource.active)
        self.assertEqual(request.originator.user, originator)
        self.assertEqual(request.status, models.Request.RequestStatus.PENDING)
        latest_transition = cast(
            models.Transition, request.transitions.order_by("-created").first()
        )
        self.assertEqual(
            latest_transition.stage.level,
            models.Stage.StageLevels.SUBMITTED,
        )

    @tag("controllers.request.create_request_user_permissions_denied")
    def test_create_request_user_permissions_denied(self) -> None:
        """Fail Case: Create a `Request` record with a `User` that
        does not have the appropriate permissions."""

        with pytest.raises(exceptions.RequestError):
            originator = AuthModels.User.objects.get(
                username=arguments.CREATE_REQUEST_USER_EMAIL_INVALID_ROLE
            )
            _ = controllers.Request.create_request(
                {
                    **arguments.BASE_CREATE_REQUEST_STRUCTURE_PARAMS,
                    "originator": originator,
                    "user": originator,
                }
            )

    @tag("controllers.request.create_request_stage_invalid")
    def test_create_request_stage_invalid(self) -> None:
        """Fail Case: Create a `Request` record with an
        invalid level for stage."""

        with pytest.raises(exceptions.RequestError):
            originator = AuthModels.User.objects.get(
                username=arguments.BASE_CREATE_REQUEST_STRUCTURE_PARAMS["originator"]
            )
            _ = controllers.Request.create_request(
                {
                    **arguments.BASE_CREATE_REQUEST_STRUCTURE_PARAMS,
                    "originator": originator,
                    "user": originator,
                    "stage": "INVALID",
                }
            )
