"""
Serializers for `ProgramMember` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from program_review_tool.models.ProgramMember import ProgramMember
from program_review_tool.models.ProgramRole.serializers import ProgramRoleSerializer
from users.models.User.serializers import UserSerializer


class ProgramMemberSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `ProgramMember`."""

    role = ProgramRoleSerializer()
    user = UserSerializer()

    class Meta:
        """Meta for `ProgramMember` serializer."""

        model = ProgramMember
        fields = "__all__"
