"""
Serializers for requests to `Record` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    """Serializer for a Task that is attached to a Record."""

    id = serializers.IntegerField(required=False, allow_null=True, default=None)
    pa_number = serializers.CharField(max_length=64)
    reporting_period = serializers.IntegerField(
        min_value=100000,
        max_value=999999,
        error_messages={
            "min_value": "Reporting period must be exactly 6 digits.",
            "max_value": "Reporting period must be exactly 6 digits.",
        },
    )
    order = serializers.IntegerField(required=False, allow_null=True, default=None)
    name = serializers.CharField(max_length=1028)
    description = serializers.CharField(max_length=4096, allow_blank=True, default="")
    owner = serializers.CharField(max_length=128)
    status = serializers.CharField(max_length=512)
    create_date = serializers.DateField()
    target_date = serializers.DateField()
    complete_date = serializers.DateField(allow_null=True, required=False, default=None)
    archive_date = serializers.DateField(allow_null=True, required=False, default=None)


class CreateRecordRequest(serializers.Serializer):
    """Request serializer for POST /v1/program-review-tool/record."""

    pa_number = serializers.CharField(max_length=1028)
    reporting_period = serializers.IntegerField(
        min_value=100000,
        max_value=999999,
        error_messages={
            "min_value": "Reporting period must be exactly 6 digits.",
            "max_value": "Reporting period must be exactly 6 digits.",
        },
    )

    name = serializers.CharField(max_length=1028, allow_blank=True, default="")
    segment = serializers.CharField(max_length=1028, allow_blank=True, default="")
    sector = serializers.CharField(max_length=1028, allow_blank=True, default="")
    division = serializers.CharField(max_length=1028, allow_blank=True, default="")
    tier = serializers.IntegerField(
        min_value=1, max_value=4, allow_null=True, default=None
    )
    program_phase = serializers.CharField(max_length=1028, allow_blank=True, default="")
    site = serializers.CharField(max_length=1028, allow_blank=True, default="")

    defense_financial_acquisition_regulation_clause = serializers.BooleanField(
        allow_null=True, default=None
    )
    cost_and_software_data_reporting_system_clause = serializers.BooleanField(
        allow_null=True, default=None
    )

    earned_value_management_system_reporting_requirement = serializers.CharField(
        max_length=1028, allow_blank=True, default=None
    )
    contract_type = serializers.CharField(max_length=1028, allow_blank=True, default="")
    contract_number = serializers.CharField(
        max_length=1028, allow_blank=True, default=""
    )
    contract_value = serializers.IntegerField(allow_null=True, default=None)
    contract_start_date = serializers.DateField(allow_null=True, default=None)
    contract_end_date = serializers.DateField(allow_null=True, default=None)

    actual_cost_work_performed_cumulative = serializers.DecimalField(
        max_digits=14, decimal_places=2, allow_null=True, default=None
    )
    budgeted_cost_work_performed_cumulative = serializers.DecimalField(
        max_digits=14, decimal_places=2, allow_null=True, default=None
    )
    budgeted_cost_work_scheduled_cumulative = serializers.DecimalField(
        max_digits=14, decimal_places=2, allow_null=True, default=None
    )
    cost_performance_index_cumulative = serializers.DecimalField(
        max_value=2, max_digits=5, decimal_places=2, allow_null=True, default=None
    )
    schedule_performance_index_cumulative = serializers.DecimalField(
        max_value=2, max_digits=5, decimal_places=2, allow_null=True, default=None
    )
    budget_at_complete = serializers.DecimalField(
        max_digits=14, decimal_places=2, allow_null=True, default=None
    )
    estimate_at_complete = serializers.DecimalField(
        max_digits=14, decimal_places=2, allow_null=True, default=None
    )
    estimate_to_complete = serializers.DecimalField(
        max_digits=14, decimal_places=2, allow_null=True, default=None
    )
    management_reserve = serializers.DecimalField(
        max_digits=14, decimal_places=2, allow_null=True, default=None
    )
    weighted_risks_and_opportunities = serializers.DecimalField(
        max_digits=14, decimal_places=2, allow_null=True, default=None
    )

    customer_assessment = serializers.IntegerField(
        min_value=1, max_value=4, allow_null=True, default=None
    )
    technical_assessment = serializers.IntegerField(
        min_value=1, max_value=4, allow_null=True, default=None
    )
    risk_assessment = serializers.IntegerField(
        min_value=1, max_value=4, allow_null=True, default=None
    )
    overall_program = serializers.IntegerField(
        min_value=1, max_value=4, allow_null=True, default=None
    )
    comments = serializers.CharField(allow_blank=True, default="")
    tasks = TaskSerializer(many=True, required=False, default=list)
    is_manual_metrics_entry = serializers.BooleanField(required=False, default=False)


class FetchRecordRequestQueryParams(serializers.Serializer):
    """Request serializer for GET /v1/program-review-tool/record query params."""

    pa_number = serializers.CharField(max_length=1028)
    reporting_period = serializers.IntegerField(
        min_value=100000,
        max_value=999999,
        error_messages={
            "min_value": "Reporting period must be exactly 6 digits.",
            "max_value": "Reporting period must be exactly 6 digits.",
        },
    )
    refresh = serializers.BooleanField(allow_null=True, default=False)
