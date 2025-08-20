"""
Serializers for `Program` model. Serializers convert
python objects to JSON.
"""

from typing import cast

from django.db.models import QuerySet
from rest_framework import serializers

from program_review_tool.models.Program import Program
from program_review_tool.models.ProgramMember import ProgramMember
from program_review_tool.models.ProgramMember.serializers import ProgramMemberSerializer


class ProgramSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Program`."""

    segment = serializers.CharField(source="segment.name", default="")

    def to_representation(self, instance: Program) -> dict:
        DECIMAL_FIELDS = (
            "actual_cost_work_performed_cumulative",
            "budgeted_cost_work_performed_cumulative",
            "budgeted_cost_work_scheduled_cumulative",
            "cost_performance_index_cumulative",
            "schedule_performance_index_cumulative",
            "budget_at_complete",
            "estimate_at_complete",
            "estimate_to_complete",
            "management_reserve",
            "weighted_risks_and_opportunities",
        )

        record: dict = super().to_representation(instance)

        instance = cast(Program, instance)
        program_members = cast(
            QuerySet[ProgramMember], instance.program_members
        ).filter(is_active=True)
        team_members = ProgramMemberSerializer(program_members, many=True).data

        for field in DECIMAL_FIELDS:
            if record[field] is not None:
                record[field] = round(float(record[field]), 2)

        record["team_members"] = team_members
        return record

    class Meta:
        """Meta for `Program` serializer."""

        model = Program
        fields = "__all__"
