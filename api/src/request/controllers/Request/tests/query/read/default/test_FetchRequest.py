"""
Collection of pytests for Request's fetch controller.
"""

import pytest
from typing import List

# pylint: disable=line-too-long
from django.db.models import QuerySet
from django.test import tag

from request.controllers.Request.Request import Request
from request.controllers.Request.tests.query.read.default import arguments
from request.exceptions import RequestError
from request.models.Request.Request import Request as RequestModel
from request.models.Request.serializers import RequestSerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "request_app",
    "request",
    "controllers.TestFetchRequest",
    "request_app.request.fetch",
    "request.fetch.default",
)
class TestFetchRequest(MultiDBTestCase):
    """Test suite for Request's fetch controller."""

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

    def setUp(self) -> None:
        super().setUp()

        self.requests_records = {}
        for request_id in arguments.FETCH_REQUEST_ALL_VALID_IDS:
            serialized_request = RequestSerializer(
                RequestModel.objects.get(id=request_id)
            ).data
            self.requests_records[request_id] = serialized_request

    @tag("controllers.request.fetch_request")
    def test_fetch_request(self) -> None:
        """Success Case: Fetch a `Request` record."""

        request = Request.fetch_requests(
            request_id=arguments.FETCH_REQUEST_BY_ID_REQUEST_ID,
            originator=None,
            stages=None,
            subfunctions=None,
            status=None,
            page=None,
            limit=None,
            include_archived=False,
        )

        data = RequestSerializer(request).data

        self.assertIsInstance(request, RequestModel)
        self.assertDictEqual(
            data, self.requests_records[arguments.FETCH_REQUEST_BY_ID_REQUEST_ID]
        )

    @tag("controllers.request.fetch_requests")
    def test_fetch_requests(self) -> None:
        """Success Case: Fetch all `Request` records."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=None,
            subfunctions=None,
            status=None,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_NON_ARCHIVED_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(request_id, arguments.FETCH_REQUEST_NON_ARCHIVED_REQUEST_IDS)

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_originator")
    def test_fetch_requests_with_originator(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            stages=None,
            subfunctions=None,
            status=None,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_WITH_ORIGINATOR_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id, arguments.FETCH_REQUEST_WITH_ORIGINATOR_REQUEST_IDS
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_originator_at_stage")
    def test_fetch_requests_with_originator_at_stage(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator at the given stage."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            stages=arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_STAGE_LEVELS,
            subfunctions=None,
            status=None,
            page=None,
            limit=None,
            include_archived=True,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_REQUEST_IDS,
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_originator_and_subfunctions")
    def test_fetch_requests_with_originator_and_subfunctions(self) -> None:
        """Success Case: Fetch all `Request` records initiated by the given
        originator with `Resource`s related to the given subfunctions."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            stages=None,
            subfunctions=arguments.FETCH_REQUEST_WITH_ORIGINATOR_AND_SUBFUNCTIONS_SUBFUNCTIONS,
            status=None,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_WITH_ORIGINATOR_AND_SUBFUNCTIONS_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AND_SUBFUNCTIONS_REQUEST_IDS,
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_originator_at_stage_with_status")
    def test_fetch_requests_with_originator_at_stage_with_status(self) -> None:
        """Success Case: Fetch all `Request` records initiated by
        the given originator at the given stage with the given
        status."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            stages=arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_STATUS_STAGE_LEVELS,
            subfunctions=None,
            status=arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_STATUS_STATUS,
            page=None,
            limit=None,
            include_archived=True,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_STATUS_REQUEST_IDS
            ),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_STATUS_REQUEST_IDS,
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_originator_subfunctions_and_status")
    def test_fetch_requests_with_originator_subfunctions_and_status(self) -> None:
        """Success Case: Fetch all `Request` records initiated by the given
        originator with `Resource`s related to the given subfunctions and with
        the given status."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            stages=None,
            subfunctions=(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_SUBFUNCTIONS_AND_STATUS_SUBFUNCTIONS
            ),
            status=arguments.FETCH_REQUEST_WITH_ORIGINATOR_SUBFUNCTIONS_AND_STATUS_STATUS,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS
            ),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS,
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag(
        "controllers.request.fetch_requests_with_originator_at_stage_with_subfunctions"
    )
    def test_fetch_requests_with_originator_at_stage_with_subfunctions(self) -> None:
        """Success Case: Fetch all `Request` records initiated by the given
        originator at the given stage with `Resource`s related to the given
        subfunctions."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            stages=arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_STAGE_LEVELS,
            subfunctions=(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_SUBFUNCTIONS
            ),
            status=None,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_REQUEST_IDS
            ),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_REQUEST_IDS,
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag(
        "controllers.request.fetch_requests_with_originator_at_stage_with_subfunctions_and_status"
    )
    def test_fetch_requests_with_originator_at_stage_with_subfunctions_and_status(
        self,
    ) -> None:
        """Success Case: Fetch all `Request` records initiated by the given originator
        at the given stage with `Resource`s related to the given subfunctions and with
        the given status."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=arguments.FETCH_REQUEST_WITH_ORIGINATOR_USER_EMAIL,
            stages=(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_STAGE_LEVELS
            ),
            subfunctions=(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_SUBFUNCTIONS
            ),
            status=(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_STATUS
            ),
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS
            ),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_ORIGINATOR_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS,
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_originator_access_dne")
    def test_fetch_requests_originator_access_dne(self) -> None:
        """Success Case: Fetch `Request` records where an appropriate
        `Access` does not exist for the given originator."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=arguments.FETCH_REQUEST_WITH_ORIGINATOR_ACCESS_DNE_USER_EMAIL,
            stages=None,
            subfunctions=None,
            status=None,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])
        self.assertEqual(
            requests.count(),  # type: ignore[union-attr]
            arguments.FETCH_REQUEST_WITH_ORIGINATOR_ACCESS_DNE,
        )

    @tag("controllers.request.fetch_requests_at_stage")
    def test_fetch_requests_at_stage(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=arguments.FETCH_REQUEST_AT_STAGE_STAGE_LEVELS,
            subfunctions=None,
            status=None,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_AT_STAGE_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(request_id, arguments.FETCH_REQUEST_AT_STAGE_REQUEST_IDS)

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_at_stage_with_subfunctions")
    def test_fetch_requests_at_stage_with_subfunctions(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage with `Resource`s related to the given subfunctions."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_STAGE_LEVELS,
            subfunctions=arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_SUBFUNCTIONS,
            status=None,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_REQUEST_IDS,
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_at_stage_with_status")
    def test_fetch_requests_at_stage_with_status(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage with the given status."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=arguments.FETCH_REQUEST_AT_STAGE_WITH_STATUS_STAGE_LEVELS,
            subfunctions=None,
            status=arguments.FETCH_REQUEST_AT_STAGE_WITH_STATUS_STATUS,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_AT_STAGE_WITH_STATUS_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id, arguments.FETCH_REQUEST_AT_STAGE_WITH_STATUS_REQUEST_IDS
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_at_stage_with_subfunctions_and_status")
    def test_fetch_requests_at_stage_with_subfunctions_and_status(self) -> None:
        """Success Case: Fetch all `Request` records at the
        given stage with `Resource`s related to the given subfunctions and
        with the given status."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_STAGE_LEVELS,
            subfunctions=arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_SUBFUNCTIONS,
            status=arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_STATUS,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(
                arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS
            ),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_AT_STAGE_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS,
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_subfunctions")
    def test_fetch_requests_with_subfunctions(self) -> None:
        """Success Case: Fetch all `Request` records with `Resource`s
        related to the given subfunctions."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=None,
            subfunctions=arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_SUBFUNCTIONS,
            status=None,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id, arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_REQUEST_IDS
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_subfunctions_and_status")
    def test_fetch_requests_with_subfunctions_and_status(self) -> None:
        """Success Case: Fetch all `Request` records with `Resource`s
        related to the given subfunctions and with the given status."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=None,
            subfunctions=arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_AND_STATUS_SUBFUNCTIONS,
            status=arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_AND_STATUS_STATUS,
            page=None,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id,
                arguments.FETCH_REQUEST_WITH_SUBFUNCTIONS_AND_STATUS_REQUEST_IDS,
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_status")
    def test_fetch_requests_with_status(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given status."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=None,
            subfunctions=None,
            status=arguments.FETCH_REQUEST_WITH_STATUS_STATUS,
            page=None,
            limit=None,
            include_archived=True,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_WITH_STATUS_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(request_id, arguments.FETCH_REQUEST_WITH_STATUS_REQUEST_IDS)

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_page")
    def test_fetch_requests_with_page(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given page."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=None,
            subfunctions=None,
            status=None,
            page=arguments.FETCH_REQUEST_WITH_PAGE_PAGE_NUMBER,
            limit=None,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_WITH_PAGE_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(request_id, arguments.FETCH_REQUEST_WITH_PAGE_REQUEST_IDS)

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_limit")
    def test_fetch_requests_with_limit(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given limit."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=None,
            subfunctions=None,
            status=None,
            page=None,
            limit=arguments.FETCH_REQUEST_WITH_LIMIT_LIMIT,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_WITH_LIMIT_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(request_id, arguments.FETCH_REQUEST_WITH_LIMIT_REQUEST_IDS)

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_page_and_limit")
    def test_fetch_requests_with_page_and_limit(self) -> None:
        """Success Case: Fetch all `Request` records with the
        given page and limit."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=None,
            subfunctions=None,
            status=None,
            page=arguments.FETCH_REQUEST_WITH_PAGE_AND_LIMIT_PAGE_NUMBER,
            limit=arguments.FETCH_REQUEST_WITH_PAGE_AND_LIMIT_LIMIT,
            include_archived=False,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_WITH_PAGE_AND_LIMIT_REQUEST_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(
                request_id, arguments.FETCH_REQUEST_WITH_PAGE_AND_LIMIT_REQUEST_IDS
            )

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_include_archived_records")
    def test_fetch_requests_include_archived_records(self) -> None:
        """Success Case: Fetch all `Request` records, including
        historical records for inactive `Resource`s."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=None,
            subfunctions=None,
            status=None,
            page=None,
            limit=None,
            include_archived=True,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            len(requests.values_list("id", flat=True)),  # type: ignore[union-attr]
            len(arguments.FETCH_REQUEST_ALL_VALID_IDS),
        )

        for request in requests:  # type: ignore[union-attr]
            self.assertIsInstance(request, RequestModel)

            request_id: int = request.id

            self.assertIn(request_id, arguments.FETCH_REQUEST_ALL_VALID_IDS)

            serialized_request = RequestSerializer(request).data
            expected_request = self.requests_records[request_id]

            self.assertEqual(serialized_request, expected_request)

    @tag("controllers.request.fetch_requests_with_page_exceeding_max_page")
    def test_fetch_requests_with_page_exceeding_max_page(self) -> None:
        """Success Case: Fetch `Request` records using a
        page number that exceeds the number of pages."""

        requests = Request.fetch_requests(
            request_id=None,
            originator=None,
            stages=None,
            subfunctions=None,
            status=None,
            page=arguments.FETCH_REQUEST_WITH_PAGE_NUMBER_EXCEEDING_PAGE_COUNT_PAGE_NUM,
            limit=None,
            include_archived=True,
        )

        self.assertIsInstance(requests, QuerySet[RequestModel])

        self.assertEqual(
            requests.count(),  # type: ignore[union-attr]
            arguments.FETCH_REQUEST_WITH_PAGE_NUMBER_EXCEEDING_PAGE_COUNT_EXPECTED_REQUESTS_COUNT,
        )

    @tag("controllers.request.fetch_request_by_id_with_page")
    def test_fetch_request_by_id_with_page(self) -> None:
        """Fail Case: Fetch a `Request` record, supplying
        a page number."""

        with pytest.raises(RequestError):
            _ = Request.fetch_requests(
                request_id=arguments.FETCH_REQUEST_BY_ID_REQUEST_ID,
                originator=None,
                stages=None,
                subfunctions=None,
                status=None,
                page=arguments.FETCH_REQUEST_WITH_PAGE_PAGE_NUMBER,
                limit=None,
                include_archived=False,
            )

    @tag("controllers.request.fetch_request_by_id_with_limit")
    def test_fetch_request_by_id_with_limit(self) -> None:
        """Fail Case: Fetch a `Request` record, supplying
        a limit."""

        with pytest.raises(RequestError):
            _ = Request.fetch_requests(
                request_id=arguments.FETCH_REQUEST_BY_ID_REQUEST_ID,
                originator=None,
                stages=None,
                subfunctions=None,
                status=None,
                page=None,
                limit=arguments.FETCH_REQUEST_WITH_LIMIT_LIMIT,
                include_archived=False,
            )

    @tag("controllers.request.fetch_request_request_dne")
    def test_fetch_request_request_dne(self) -> None:
        """Fail Case: Fetch a `Request` record where the record
        does not exist for the given id."""

        with pytest.raises(RequestError):
            _ = Request.fetch_requests(
                request_id=arguments.FETCH_REQUEST_BY_ID_REQUEST_ID_DNE,
                originator=None,
                stages=None,
                subfunctions=None,
                status=None,
                page=None,
                limit=None,
                include_archived=False,
            )

    @tag("controllers.request.fetch_requests_originator_dne")
    def test_fetch_requests_originator_dne(self) -> None:
        """Fail Case: Fetch `Request` records where a `User`
        does not exist for the given originator."""

        with pytest.raises(RequestError):
            _ = Request.fetch_requests(
                request_id=None,
                originator=arguments.FETCH_REQUEST_WITH_ORIGINATOR_DNE_USER_EMAIL,
                stages=None,
                subfunctions=None,
                status=None,
                page=None,
                limit=None,
                include_archived=False,
            )
