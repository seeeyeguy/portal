"""
Collection of pytests for RequestNotification's fetch view endpoint.
"""

from typing import List

# pylint: disable=line-too-long
from django.test import tag
from django.urls import reverse
from rest_framework import status

from request.controllers.Request.tests.query.read.serialized import arguments


from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "request_app",
    "request",
    "views",
    "request_app.request_notification.fetch",
    "request_notification.fetch.serialized",
    "views.TestFetchRequestNotification",
)
class TestFetchRequestNotification(MultiDBTestCase):
    """
    Tests for GET /v1/request/request-notification endpoint.
    """

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "request/controllers/Request/tests/query/read/serialized/fixtures/resources.json",
        "request/controllers/Request/tests/query/read/serialized/fixtures/pointofcontacts.json",
        "request/controllers/Request/tests/query/read/serialized/fixtures/requests.json",
        "request/controllers/Request/tests/query/read/serialized/fixtures/transitions.json",
        "request/controllers/Request/tests/query/read/serialized/fixtures/dispositions.json",
    ]

    url: str = reverse("request.request_notification")

    @tag("views.request_notification.fetch_request_notification")
    def test_fetch_request_notification(self) -> None:
        """Success Case: Fetch `Request` notifications."""

        response = self.client.get(
            self.url, headers={"content_type": "application/json"}
        )

        request_notifications = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertListEqual(
            request_notifications,
            arguments.FETCH_REQUEST_NOTIFICATION_EXPECTED_NOTIFICATIONS,
        )
