"""
Collection of pytests for Usages fetch controller.
"""
from django.test import tag
from django.db.models import QuerySet
from program_review_tool.controllers.Usage.Usage import Usage
from analytics import exceptions
from manager.utils.tests import MultiDBTestCase
from program_review_tool.controllers.Usage.tests.query.read.default import arguments


@tag(
    "program_review_tool",
    "usage",
    "controllers",
    "program_review_tool.usage.fetch",
    "usage.fetch.default",
    "controllers.TestFetchUsage",
)
class TestFetchUsage(MultiDBTestCase):
    fixtures = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Usage/tests/query/read/default/fixtures/usage_data.json",
    ]

    @tag("controllers.usage.fetch")
    def test_fetch_usage(self) -> None:
        """Success Case: Fetch all Usage records for a valid user without pagination."""
        usage_queries = Usage.fetch_usage(
            user=arguments.FETCH_USAGE_USER,
            page=None,
            limit=None,
        )
        self.assertIsInstance(usage_queries, QuerySet)

    def test_fetch_with_page_and_limit(self) -> None:
        """Success Case: Fetch Usage records with valid page + limit pagination."""
        results = Usage.fetch_usage(
            user=arguments.FETCH_USAGE_USER,
            page=arguments.FETCH_USAGE_PAGE,
            limit=arguments.FETCH_USAGE_LIMIT,
        )
        self.assertIsInstance(results, QuerySet)
        self.assertEqual(results.count(), arguments.FETCH_USAGE_LIMIT)

    def test_fetch_with_limit_only(self) -> None:
        """Success Case: Fetch Usage records with only limit applied."""
        results = Usage.fetch_usage(
            user=arguments.FETCH_USAGE_USER,
            limit=arguments.FETCH_USAGE_LIMIT,
        )
        self.assertIsInstance(results, QuerySet)
        self.assertLessEqual(results.count(), arguments.FETCH_USAGE_LIMIT)

    def test_fetch_invalid_user(self) -> None:
        """Fail Case: Attempt to fetch Usage records for an invalid user email."""
        with self.assertRaises(exceptions.AnalyticsError) as exc_info:
            Usage.fetch_usage(user=arguments.INVALID_USER)
        self.assertIn(arguments.FETCH_USAGE_ERROR_INVALID_USER, str(exc_info.exception))

    def test_fetch_with_negative_page(self) -> None:
        """Fail Case: Page must be a positive integer."""
        with self.assertRaises(exceptions.AnalyticsError) as exc_info:
            Usage.fetch_usage(
                user=arguments.FETCH_USAGE_USER,
                page=-1,
                limit=arguments.FETCH_USAGE_LIMIT,
            )
        self.assertIn("Page must be a positive integer", str(exc_info.exception))

    def test_fetch_with_negative_limit(self) -> None:
        """Fail Case: Limit must be a positive integer."""
        with self.assertRaises(exceptions.AnalyticsError) as exc_info:
            Usage.fetch_usage(
                user=arguments.FETCH_USAGE_USER,
                page=arguments.FETCH_USAGE_PAGE,
                limit=arguments.INVALID_USAGE_LIMIT,
            )
        self.assertIn("Limit must be a positive integer", str(exc_info.exception))

    def test_fetch_with_pa_number(self) -> None:
        """Success Case: Fetch Usage records filtered by a specific PA number."""
        results = Usage.fetch_usage(
            user=arguments.FETCH_USAGE_USER,
            pa_number=arguments.FETCH_USAGE_PA_NUMBER,
        )
        self.assertIsInstance(results, QuerySet)
        for usage in results:
            self.assertIn(arguments.FETCH_USAGE_PA_NUMBER, usage.programs)

    def test_fetch_with_invalid_pa_number(self) -> None:
        """Fail Case: Fetch Usage records with a non-existent PA number returns empty queryset."""
        results = Usage.fetch_usage(
            user=arguments.FETCH_USAGE_USER,
            pa_number=arguments.FETCH_USAGE_INVALID_PA_NUMBER,
        )
        self.assertEqual(results.count(), 0)

    def test_fetch_successful_usages(self) -> None:
        """Success Case: Fetch Usage records where success=True."""
        results = Usage.fetch_usage(
            user=arguments.FETCH_USAGE_USER,
            success=arguments.FETCH_USAGE_SUCCESS_TRUE,
        )
        self.assertIsInstance(results, QuerySet)
        for usage in results:
            self.assertTrue(usage.success)

    def test_fetch_failed_usages(self) -> None:
        """Success Case: Fetch Usage records where success=False."""
        results = Usage.fetch_usage(
            user=arguments.FETCH_USAGE_USER,
            success=arguments.FETCH_USAGE_SUCCESS_FALSE,
        )
        self.assertIsInstance(results, QuerySet)
        for usage in results:
            self.assertFalse(usage.success)
