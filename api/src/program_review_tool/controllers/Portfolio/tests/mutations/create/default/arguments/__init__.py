"""
Arguments to be shared for Portfolio's create
controller pytests.
"""

from typing import List

CREATE_PORTFOLIO_USER_EMAIL: str = "May.Parker@harris.com"

CREATE_PORTFOLIO_NAME: str = "New Portfolio Name 1"

CREATE_PORTFOLIO_PROGRAM_IDS: List[int] = [1, 2]

CREATE_PORTFOLIO_DUPLICATE_NAME_FOR_USER: str = "Existing Portfolio Name"

CREATE_PORTFOLIO_PROGRAM_IDS_DNE: List[int] = [99, 999]

CREATE_PORTFOLIO_EXPECTED_PORTFOLIO: dict = {
    "id": 2,
    "name": "New Portfolio Name 1",
    "user": {
        "id": 1,
        "username": "May.Parker@harris.com",
        "email": "May.Parker@l3harris.com",
        "first_name": "May",
        "last_name": "Parker",
        "is_active": True,
    },
    "programs": [
        {
            "id": 1,
            "segment": "SPACE & AIRBORNE SYSTEMS",
            "name": "SOA IDIQ II_6C27",
            "created": "2025-01-01T11:00:00-05:00",
            "modified": "2025-01-01T11:00:00-05:00",
            "pa_number": "6C27",
            "sector": "Airborne Combat Systems",
            "division": "Electronic Warfare",
            "tier": 1,
            "contract_type": "FFP",
            "contract_number": "CN865247",
            "contract_value": 1000000000,
            "contract_start_date": "2025-01-01",
            "contract_end_date": "2025-12-01",
            "actual_cost_work_performed_cumulative": 70.36,
            "budgeted_cost_work_performed_cumulative": 20.55,
            "budgeted_cost_work_scheduled_cumulative": 59.46,
            "cost_performance_index_cumulative": 0.02,
            "schedule_performance_index_cumulative": 0.32,
            "budget_at_complete": 41.97,
            "estimate_at_complete": 84.95,
            "estimate_to_complete": 36.02,
            "management_reserve": 47.9,
            "weighted_risks_and_opportunities": 30.27,
            "active_status": True,
            "team_members": [],
        },
        {
            "id": 2,
            "segment": "SPACE & AIRBORNE SYSTEMS",
            "name": "Zeus CLIN 0005 Single Launch_10LR",
            "created": "2025-01-01T11:00:00-05:00",
            "modified": "2025-01-01T11:00:00-05:00",
            "pa_number": "10LR",
            "sector": "Space Systems",
            "division": "Surveillance Systems",
            "tier": 3,
            "contract_type": "FFP",
            "contract_number": "CN323301",
            "contract_value": 2000000000,
            "contract_start_date": "2025-01-01",
            "contract_end_date": "2025-12-01",
            "actual_cost_work_performed_cumulative": 77.02,
            "budgeted_cost_work_performed_cumulative": 52.81,
            "budgeted_cost_work_scheduled_cumulative": 53.5,
            "cost_performance_index_cumulative": 1.75,
            "schedule_performance_index_cumulative": 0.31,
            "budget_at_complete": 46.33,
            "estimate_at_complete": 98.95,
            "estimate_to_complete": 54.6,
            "management_reserve": 29.55,
            "weighted_risks_and_opportunities": 72.65,
            "active_status": True,
            "team_members": [],
        },
    ],
}
