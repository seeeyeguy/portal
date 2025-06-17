"""
Collection of pytests for Request's delete controller.
"""

import pytest
from typing import cast, List

from django.contrib.auth import models as AuthModels
from django.test import tag

from directory import models as DirectoryModels
from request import controllers, exceptions, models
from request.controllers.Request.tests.mutations.delete.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "request_app",
    "request",
    "controllers.TestDeleteRequest",
    "request_app.request.delete",
    "request.delete.default",
)
class TestDeleteRequest(MultiDBTestCase):
    """Test suite for Request's delete controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "request/controllers/Request/tests/mutations/delete/default/fixtures/users.json",
        "request/controllers/Request/tests/mutations/delete/default/fixtures/resources.json",
        "request/controllers/Request/tests/mutations/delete/default/fixtures/pointofcontacts.json",
        "request/controllers/Request/tests/mutations/delete/default/fixtures/requests.json",
        "request/controllers/Request/tests/mutations/delete/default/fixtures/transitions.json",
        "request/controllers/Request/tests/mutations/delete/default/fixtures/dispositions.json",
    ]

    @tag("controllers.request.delete_request")
    def test_delete_request(self) -> None:
        """Success Case: Create a delete `Request` record."""

        originator = AuthModels.User.objects.get(
            email=arguments.BASE_DELETE_REQUEST_STRUCTURE_PARAMS["originator"]
        )

        request = controllers.Request.delete_request(
            {
                **arguments.BASE_DELETE_REQUEST_STRUCTURE_PARAMS,
                "originator": originator,
            }
        )

        self.assertIsInstance(request, models.Request)
        self.assertTrue(request.resource)
        self.assertIsInstance(request.resource, DirectoryModels.Resource)
        self.assertFalse(request.resource.active)
        self.assertTrue(request.resource.deleted)
        self.assertEqual(request.originator.user, originator)
        self.assertEqual(request.status, models.Request.RequestStatus.PENDING)
        latest_transition = cast(
            models.Transition, request.transitions.order_by("-created").first()
        )
        self.assertEqual(
            latest_transition.stage.level,
            models.Stage.StageLevels.SUBMITTED,
        )

    @tag("controllers.request.delete_request_user_permissions_denied")
    def test_create_request_user_permissions_denied(self) -> None:
        """Fail Case: Create a `Request` record with a `User` that
        does not have the appropriate permissions."""

        with pytest.raises(exceptions.RequestError):
            originator = AuthModels.User.objects.get(
                email=arguments.DELETE_REQUEST_USER_EMAIL_INVALID_ROLE
            )
            _ = controllers.Request.delete_request(
                {
                    **arguments.BASE_DELETE_REQUEST_STRUCTURE_PARAMS,
                    "originator": originator,
                }
            )

    @tag("controllers.request.delete_request_already_exists")
    def test_delete_request_request_already_exists(self) -> None:
        """Fail Case: Create a delete `Request` record for a `Resource` that
        already has an open request."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Request.delete_request(
                {
                    **arguments.BASE_DELETE_REQUEST_STRUCTURE_PARAMS,
                    "resource_id": arguments.DELETE_REQUEST_RESOURCE_ID_HAS_REQUEST_OPEN,
                }
            )

    @tag("controllers.request.delete_request_resource_dne")
    def test_delete_request_resource_dne(self) -> None:
        """Fail Case: Create a delete `Request` where
        the `Resource` does not exist for the given id."""

        with pytest.raises(exceptions.RequestError):
            _ = controllers.Request.delete_request(
                {
                    **arguments.BASE_DELETE_REQUEST_STRUCTURE_PARAMS,
                    "resource_id": 999,
                }
            )
