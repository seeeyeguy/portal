
"""
Serializers for requests to `JobRun` views. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers


class CreateJobRunRequest(serializers.Serializer):
    """Request serializer for POST /v1/program-review-tool/jobrun."""

    job_name = serializers.CharField(max_length=2048)

class FetchJobRunRequest(serializers.Serializer):
    """Request serializer for GET /v1/program-reivew/tool/jobrun."""

    id = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    user = serializers.EmailField(allow_blank=True, default="")
    page = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    limit = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    status = serializers.BooleanField(allow_null=True, default=None)
