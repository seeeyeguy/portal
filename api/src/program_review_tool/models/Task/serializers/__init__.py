"""
Serializers for `Task` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from program_review_tool.models.Task import Task


class TaskSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Task`."""

    name = serializers.CharField(source="task_name", read_only=False)

    class Meta:
        """Meta for `Task` serializer."""

        model = Task
        fields = [
            "id",
            "name",
            "description",
            "status",
            "order",
            "owner",
            "pa_number",
            "reporting_period",
            "create_date",
            "target_date",
            "complete_date",
            "archive_date",
        ]
