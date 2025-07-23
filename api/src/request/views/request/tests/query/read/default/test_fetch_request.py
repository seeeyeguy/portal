"""
Collection of pytests for Request's fetch view endpoint.
"""

from typing import List

# pylint: disable=line-too-long
from django.test import tag
from django.urls import reverse
from rest_framework import status

from request.controllers.Request.tests.query.read.default import arguments
from request.models.Request.Request import Request as RequestModel
from request.models.Request.serializers import RequestSerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "request_app",
    "request",
    "views",
    "request_app.request.fetch",
    "request.fetch.default",
    "views.TestFetchRequest",
)
class TestFetchRequest(MultiDBTestCase):
    """
    Tests for GET /v1/request/request endpoint.
    """

    def setUp(self) -> None:

        super().setUp()

        self.requests_records = {}
        for request_id in arguments.FETCH_REQUEST_ALL_VALID_IDS:
            serialized_request = RequestSerializer(
                RequestModel.objects.get(id=request_id)
            ).data
            self.requests_records[request_id] = serialized_request

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "request/controllers/Request/tests/query/read/default/fixtures/users.json",
        "request/controllers/Request/tests/query/read/default/fixtures/accesses.json",
        "request/controllers/Request/tests/query/read/default/fixtures/resources.json",
        "request/controllers/Request/tests/query/read/default/fixtures/pointofcontacts.json",
        "request/controllers/Request/tests/query/read/default/fixtures/requests.json",
        "request/controllers/Request/tests/query/read/default/fixtures/transitions.json",
        "request/controllers/Request/tests/query/read/default/fixtures/dispositions.json",
    ]

    url: str = reverse("request.request")

    @tag("views.request.fetch_request")
    def test_fetch_request(self) -> None:
        """Success Case: Fetch a `Request` record."""

        params: dict = {
            "id": arguments.FETCH_REQUEST_BY_ID_REQUEST_ID,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        request = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(request, dict)

        self.assertEqual(
            request, self.requests_records[arguments.FETCH_REQUEST_BY_ID_REQUEST_ID]
        )

    @tag("views.request.fetch_requests")
    def test_fetch_requests(self) -> None:
        """Success Case: Fetch all `Request` records."""

        response = self.client.get(
            self.url, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests), len(arguments.FETCH_REQUEST_NON_ARCHIVED_REQUEST_IDS)
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(request_id, arguments.FETCH_REQUEST_NON_ARCHIVED_REQUEST_IDS)

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_originator")
    def test_fetch_requests_with_originator(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator."""

        params: dict = {
            "originator": arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests), len(arguments.FETCH_REQUEST_WITH_ORIGINATOR_REQUEST_IDS)
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id, arguments.FETCH_REQUEST_WITH_ORIGINATOR_REQUEST_IDS
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_originator_at_stage")
    def test_fetch_requests_with_originator_at_stage(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator at the given stage."""

        params: dict = {
            "originator": arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            "stages": arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_STAGE_LEVELS,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            len(arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_REQUEST_IDS),
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id, arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_REQUEST_IDS
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_originator_and_subfunctions")
    def test_fetch_requests_with_originator_and_subfunctions(self) -> None:
        """Success Case: Fetch all `Request` records initiated by the given
        originator with `Resource`s related to the given subfunctions."""

        params: dict = {
            "originator": arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            "subfunctions": arguments.FETCH_REQUEST_WITH_ORIGINATOR_AND_SUBFUNCTIONS_SUBFUNCTIONS,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            len(arguments.FETCH_REQUEST_WITH_ORIGINATOR_AND_SUBFUNCTIONS_REQUEST_IDS),
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AND_SUBFUNCTIONS_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_originator_at_stage_with_status")
    def test_fetch_requests_with_originator_at_stage_with_status(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator at the given stage with the given
        status."""

        params: dict = {
            "originator": arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            "stages": arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_STATUS_STAGE_LEVELS,
            "status": arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_STATUS_STATUS,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            len(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_STATUS_REQUEST_IDS
            ),
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_STATUS_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_originator_subfunctions_and_status")
    def test_fetch_requests_with_originator_subfunctions_and_status(self) -> None:
        """Success Case: Fetch all `Request` records initiated by the given
        originator with `Resource`s related to the given subfunctions and with
        the given status."""

        params: dict = {
            "originator": arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            "subfunctions": arguments.FETCH_REQUEST_WITH_ORIGINATOR_SUBFUNCTIONS_AND_STATUS_SUBFUNCTIONS,
            "status": arguments.FETCH_REQUEST_WITH_ORIGINATOR_SUBFUNCTIONS_AND_STATUS_STATUS,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            len(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS
            ),
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_originator_at_stage_with_subfunctions")
    def test_fetch_requests_with_originator_at_stage_with_subfunctions(self) -> None:
        """Success Case: Fetch all `Request` records initiated by the given
        originator at the given stage with `Resource`s related to the given
        subfunctions."""

        params: dict = {
            "originator": arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            "stages": arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_STAGE_LEVELS,
            "subfunctions": arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_SUBFUNCTIONS,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            len(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_REQUEST_IDS
            ),
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag(
        "views.request.fetch_requests_with_originator_at_stage_with_subfunctions_and_status"
    )
    def test_fetch_requests_with_originator_at_stage_with_subfunctions_and_status(
        self,
    ) -> None:
        """Success Case: Fetch all `Request` records initiated by the given originator
        at the given stage with `Resource`s related to the given subfunctions and with
        the given status."""

        params: dict = {
            "originator": arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            "stages": arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_STAGE_LEVELS,
            "subfunctions": arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_SUBFUNCTIONS,
            "status": arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_STATUS,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            len(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS
            ),
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_originator_access_dne")
    def test_fetch_requests_originator_access_dne(self) -> None:
        """Success Case: Fetch `Request` records where an appropriate
        `Access` does not exist for the given originator."""

        params: dict = {
            "originator": arguments.FETCH_REQUEST_WITH_ORIGINATOR_ACCESS_DNE_USER_EMAIL,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            arguments.FETCH_REQUEST_WITH_ORIGINATOR_ACCESS_DNE,
        )

    @tag("views.request.fetch_requests_at_stage")
    def test_fetch_requests_at_stage(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage."""

        params: dict = {
            "stages": arguments.FETCH_REQUEST_AT_STAGE_STAGE_LEVELS,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests), len(arguments.FETCH_REQUEST_AT_STAGE_REQUEST_IDS)
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_AT_STAGE_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_at_stage_with_subfunctions")
    def test_fetch_requests_at_stage_with_subfunctions(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage with `Resource`s related to the given subfunctions."""

        params: dict = {
            "stages": arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_STAGE_LEVELS,
            "subfunctions": arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_SUBFUNCTIONS,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            len(arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_REQUEST_IDS),
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_at_stage_with_status")
    def test_fetch_requests_at_stage_with_status(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage with the given status."""

        params: dict = {
            "stages": arguments.FETCH_REQUEST_AT_STAGE_WITH_STATUS_STAGE_LEVELS,
            "status": arguments.FETCH_REQUEST_AT_STAGE_WITH_STATUS_STATUS,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests), len(arguments.FETCH_REQUEST_AT_STAGE_WITH_STATUS_REQUEST_IDS)
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_AT_STAGE_WITH_STATUS_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_at_stage_with_subfunctions_and_status")
    def test_fetch_requests_at_stage_with_subfunctions_and_status(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage with `Resource`s related to the given subfunctions and
        with the given status."""

        params: dict = {
            "stages": arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_STAGE_LEVELS,
            "subfunctions": arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_SUBFUNCTIONS,
            "status": arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_STATUS,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            len(
                arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS
            ),
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_subfunctions")
    def test_fetch_requests_with_subfunctions(self) -> None:
        """Success Case: Fetch all `Request` records with `Resource`s
        related to the given subfunctions."""

        params: dict = {
            "subfunctions": arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_SUBFUNCTIONS
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            len(arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_REQUEST_IDS),
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_subfunctions_and_status")
    def test_fetch_requests_with_subfunctions_and_status(self) -> None:
        """Success Case: Fetch all `Request` records with `Resource`s
        related to the given subfunctions and with the given status."""

        params: dict = {
            "subfunctions": arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_AND_STATUS_SUBFUNCTIONS,
            "status": arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_AND_STATUS_STATUS,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            len(arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS),
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_status")
    def test_fetch_requests_with_status(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given status."""

        params: dict = {"status": arguments.FETCH_REQUEST_WITH_STATUS_STATUS}

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests), len(arguments.FETCH_REQUEST_WITH_STATUS_REQUEST_IDS)
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_STATUS_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_page")
    def test_fetch_requests_with_page(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given page."""

        params: dict = {
            "page": arguments.FETCH_REQUEST_WITH_PAGE_PAGE_NUMBER,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests), len(arguments.FETCH_REQUEST_WITH_PAGE_REQUEST_IDS)
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_PAGE_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_limit")
    def test_fetch_requests_with_limit(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given limit."""

        params: dict = {
            "limit": arguments.FETCH_REQUEST_WITH_LIMIT_LIMIT,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests), len(arguments.FETCH_REQUEST_WITH_LIMIT_REQUEST_IDS)
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_LIMIT_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_page_and_limit")
    def test_fetch_requests_with_page_and_limit(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given page and limit."""

        params: dict = {
            "page": arguments.FETCH_REQUEST_WITH_PAGE_AND_LIMIT_PAGE_NUMBER,
            "limit": arguments.FETCH_REQUEST_WITH_PAGE_AND_LIMIT_LIMIT,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests), len(arguments.FETCH_REQUEST_WITH_PAGE_AND_LIMIT_REQUEST_IDS)
        )

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_PAGE_AND_LIMIT_REQUEST_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_include_archived_records")
    def test_fetch_requests_include_archived_records(self) -> None:
        """Success Case: Fetch all `Request` records, including
        historical records for inactive `Resource`s."""

        params: dict = {
            "include_archived": True,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(len(requests), len(arguments.FETCH_REQUEST_ALL_VALID_IDS))

        for request in requests:
            self.assertIsInstance(request, dict)

            request_id: int = request["id"]

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_ALL_VALID_IDS,
            )

            expected_request = self.requests_records[request_id]

            self.assertEqual(request, expected_request)

    @tag("views.request.fetch_requests_with_page_exceeding_max_page")
    def test_fetch_requests_with_page_exceeding_max_page(self) -> None:
        """Success Case: Fetch `Request` records using a
        page number that exceeds the number of pages."""

        params: dict = {
            "page": arguments.FETCH_REQUEST_WITH_PAGE_NUMBER_EXCEEDING_PAGE_COUNT_PAGE_NUM,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        requests = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(requests, list)

        self.assertEqual(
            len(requests),
            arguments.FETCH_REQUEST_WITH_PAGE_NUMBER_EXCEEDING_PAGE_COUNT_EXPECTED_REQUESTS_COUNT,
        )

    @tag("views.request.fetch_request_by_id_with_page")
    def test_fetch_request_by_id_with_page(self) -> None:
        """Fail Case: Fetch a `Request` record, supplying
        a page number."""

        params: dict = {
            "id": arguments.FETCH_REQUEST_BY_ID_REQUEST_ID,
            "page": arguments.FETCH_REQUEST_WITH_PAGE_PAGE_NUMBER,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.request.fetch_request_by_id_with_limit")
    def test_fetch_request_by_id_with_limit(self) -> None:
        """Fail Case: Fetch a `Request` record, supplying
        a limit."""

        params: dict = {
            "id": arguments.FETCH_REQUEST_BY_ID_REQUEST_ID,
            "limit": arguments.FETCH_REQUEST_WITH_LIMIT_LIMIT,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.request.fetch_request_request_dne")
    def test_fetch_request_request_dne(self) -> None:
        """Fail Case: Fetch a `Request` record where the record
        does not exist for the given id."""

        params: dict = {
            "id": arguments.FETCH_REQUEST_BY_ID_REQUEST_ID_DNE,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.request.fetch_requests_originator_dne")
    def test_fetch_requests_originator_dne(self) -> None:
        """Fail Case: Fetch `Request` records where a `User`
        does not exist for the given originator."""

        params: dict = {
            "originator": arguments.FETCH_REQUEST_WITH_ORIGINATOR_DNE_USER_EMAIL,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
