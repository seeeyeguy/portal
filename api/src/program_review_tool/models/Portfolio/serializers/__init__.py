"""
Serializers for `Portfolio` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from program_review_tool.models.Portfolio import Portfolio

from program_review_tool.models.Program.serializers import ProgramSerializer
from users.models.User.serializers import UserSerializer


class PortfolioSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Portfolio`."""

    user = UserSerializer(read_only=True)
    programs = ProgramSerializer(many=True, read_only=True)

    class Meta:
        """Meta for `Portfolio` serializer."""

        model = Portfolio
        fields = "__all__"
