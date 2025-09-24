"""
Serializers for requests to `ReportingPeriod` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class FetchReportingPeriodRequest(serializers.Serializer):
    """Request serializer for GET /v1/program-review-tool/reporting-period."""

    previous_period_count = serializers.IntegerField(
        min_value=0,
        allow_null=True,
        default=None,
    )
