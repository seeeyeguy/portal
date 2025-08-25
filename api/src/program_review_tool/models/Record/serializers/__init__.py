"""
Serializers for `Record` model. Serializers convert
python objects to JSON.
"""


from rest_framework import serializers

from program_review_tool.models.Record import Record

from program_review_tool.models.Program.serializers import ProgramSerializer
from program_review_tool.models.ProgramMember.serializers import ProgramMemberSerializer
from users.models.User.serializers import UserSerializer


class RecordSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Record`."""

    user = UserSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)
    team_members = ProgramMemberSerializer(many=True, read_only=True)

    def to_representation(self, instance: Record) -> dict:
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

        # Let the parent class build the initial dict
        record: dict = super().to_representation(instance)

        # Cast any non‑null Decimals to float (rounded to 2 dp)
        for field in DECIMAL_FIELDS:
            value = record.get(field)
            if value is not None:
                record[field] = round(float(value), 2)

        return record

    class Meta:
        """Meta for `Record` serializer."""

        model = Record
        fields = "__all__"
