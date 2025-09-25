"""
Serializers for `Task` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from program_review_tool.models.Task import Task

from program_review_tool.models.Program.serializers import ProgramSerializer
from users.models.User.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Task`."""

    user = UserSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)

    class Meta:
        """Meta for `Task` serializer."""

        model = Task
        fields = "__all__"
