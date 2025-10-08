"""
Collection of pytests for RequestNotification's fetch controller.
"""

import pytest
from typing import List

# pylint: disable=line-too-long
from django.test import tag

from request.controllers.Request.Request import RequestNotification
from request.controllers.Request.tests.query.read.serialized import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "request_app",
    "request_notification",
    "controllers.TestFetchRequestNotification",
    "request_app.request_notification.fetch",
    "request_notification.fetch.serialized",
)
class TestFetchRequestNotification(MultiDBTestCase):
    """Test suite for RequestNotification's fetch controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "request/controllers/Request/tests/query/read/serialized/fixtures/resources.json",
        "request/controllers/Request/tests/query/read/serialized/fixtures/pointofcontacts.json",
        "request/controllers/Request/tests/query/read/serialized/fixtures/requests.json",
        "request/controllers/Request/tests/query/read/serialized/fixtures/transitions.json",
        "request/controllers/Request/tests/query/read/serialized/fixtures/dispositions.json",
    ]

    @tag("controllers.request_notification.fetch_request_notification")
    def test_fetch_request_notification(self) -> None:
        """Success Case: Fetch `Request` notifications."""

        request_notifications = RequestNotification.fetch_request_notifications()

        self.assertListEqual(
            request_notifications,
            arguments.FETCH_REQUEST_NOTIFICATION_EXPECTED_NOTIFICATIONS,
        )
