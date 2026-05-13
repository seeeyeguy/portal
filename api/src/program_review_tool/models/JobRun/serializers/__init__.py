"""
Serializers for `JobRun` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from program_review_tool.models.JobRun import JobRun


class JobRunSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `JobRun`."""

    class Meta:
        """Meta for `JobRun` serializer."""

        model = JobRun
        fields = "__all__"
