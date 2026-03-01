"""
Collection of pytests for Request's update controller.
"""

import pytest
from typing import cast, List

from django.contrib.auth import models as AuthModels
from django.test import tag

from directory import models as DirectoryModels
from request import controllers, exceptions, models
from request.controllers.Request.tests.mutations.update.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "request_app",
    "request",
    "controllers.TestUpdateRequest",
    "request_app.request.update",
    "request.update.default",
)
class TestUpdateRequest(MultiDBTestCase):
    """Test suite for Request's update controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "request/controllers/Request/tests/mutations/update/default/fixtures/users.json",
        "request/controllers/Request/tests/mutations/update/default/fixtures/resources.json",
        "request/controllers/Request/tests/mutations/update/default/fixtures/pointofcontacts.json",
        "request/controllers/Request/tests/mutations/update/default/fixtures/requests.json",
        "request/controllers/Request/tests/mutations/update/default/fixtures/transitions.json",
    ]

    @tag("controllers.request.update_request")
    def test_update_request(self) -> None:
        """Success Case: Update a `Request` record."""

        requester = AuthModels.User.objects.get(
            username=arguments.UPDATE_REQUEST_USER_EMAIL
        )

        updated_request, rows_affected = controllers.Request.update_request(
            {
                **arguments.BASE_UPDATE_REQUEST_STRUCTURE_PARAMS,
                "user": requester,
            }
        )

        self.assertEqual(rows_affected, 1)
        self.assertIsInstance(updated_request, models.Request)
        self.assertTrue(updated_request.resource)
        self.assertIsInstance(updated_request.resource, DirectoryModels.Resource)
        self.assertFalse(updated_request.resource.active)
        self.assertEqual(updated_request.originator.user, requester)
        self.assertEqual(updated_request.status, models.Request.RequestStatus.PENDING)
        latest_transition = cast(
            models.Transition, updated_request.transitions.order_by("-created").first()
        )
        self.assertEqual(
            latest_transition.stage.level,
            models.Stage.StageLevels.DRAFT,
        )

    @tag("controllers.request.update_request_submitted")
    def test_update_request_submitted(self) -> None:
        """Success Case: Update and submit a `Request` record."""

        requester = AuthModels.User.objects.get(
            username=arguments.UPDATE_REQUEST_USER_EMAIL
        )

        updated_request, rows_affected = controllers.Request.update_request(
            {
                **arguments.BASE_UPDATE_REQUEST_STRUCTURE_PARAMS,
                "user": requester,
                "stage": "SUBMITTED",
            }
        )

        self.assertEqual(rows_affected, 1)
        self.assertIsInstance(updated_request, models.Request)
        self.assertTrue(updated_request.resource)
        self.assertIsInstance(updated_request.resource, DirectoryModels.Resource)
        self.assertFalse(updated_request.resource.active)
        self.assertEqual(updated_request.originator.user, requester)
        self.assertEqual(updated_request.status, models.Request.RequestStatus.PENDING)
        latest_transition = cast(
            models.Transition, updated_request.transitions.order_by("-created").first()
        )
        self.assertEqual(
            latest_transition.stage.level,
            models.Stage.StageLevels.SUBMITTED,
        )

    @tag("controllers.request.update_request_user_permissions_denied")
    def test_update_request_user_permissions_denied(self) -> None:
        """Fail Case: Create a `Request` record with a `User` that
        does not have the appropriate permissions."""

        with pytest.raises(exceptions.RequestError):
            requester = AuthModels.User.objects.get(
                username=arguments.UPDATE_REQUEST_USER_EMAIL_INVALID_ROLE
            )
            _ = controllers.Request.update_request(
                {
                    **arguments.BASE_UPDATE_REQUEST_STRUCTURE_PARAMS,
                    "user": requester,
                }
            )

    @tag("controllers.request.update_request_user_not_originator")
    def test_update_request_user_not_originator(self) -> None:
        """Fail Case: Create a `Request` record with a `User` that
        does not have the appropriate permissions."""

        with pytest.raises(exceptions.RequestError):
            requester = AuthModels.User.objects.get(
                username=arguments.UPDATE_REQUEST_USER_EMAIL_NOT_ORIGINATOR
            )
            _ = controllers.Request.update_request(
                {
                    **arguments.BASE_UPDATE_REQUEST_STRUCTURE_PARAMS,
                    "user": requester,
                }
            )

    @tag("controllers.request.update_request_request_dne")
    def test_update_request_request_dne(self) -> None:
        """Fail Case: Update a `Request` record where
        the record does not exist for the given id."""

        with pytest.raises(exceptions.RequestError):
            requester = AuthModels.User.objects.get(
                username=arguments.UPDATE_REQUEST_USER_EMAIL
            )
            _ = controllers.Request.update_request(
                {
                    **arguments.BASE_UPDATE_REQUEST_STRUCTURE_PARAMS,
                    "request_id": arguments.INVALID_UPDATE_REQUEST_ID_DNE,
                    "user": requester,
                }
            )

    @tag("controllers.request.update_request_stage_invalid")
    def test_update_request_stage_invalid(self) -> None:
        """Fail Case: Update a `Request` record with an
        invalid value for stage."""

        with pytest.raises(exceptions.RequestError):
            requester = AuthModels.User.objects.get(
                username=arguments.UPDATE_REQUEST_USER_EMAIL
            )
            _ = controllers.Request.update_request(
                {
                    **arguments.BASE_UPDATE_REQUEST_STRUCTURE_PARAMS,
                    "user": requester,
                    "stage": "INVALID",
                }
            )

    @tag("controllers.request.update_request_transition_stage_invalid")
    def test_update_request_transition_stage_invalid(self) -> None:
        """Fail Case: Update a `Request` record currently with a latest
        transition in the `Stage` (`SUBMITTED`)."""

        with pytest.raises(exceptions.RequestError):
            requester = AuthModels.User.objects.get(
                username=arguments.UPDATE_REQUEST_USER_EMAIL
            )
            _ = controllers.Request.update_request(
                {
                    **arguments.BASE_UPDATE_REQUEST_STRUCTURE_PARAMS,
                    "request_id": arguments.INVALID_UPDATE_REQUEST_ID_SUBMITTED,
                    "user": requester,
                }
            )
