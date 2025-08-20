"""
Arguments to be shared for Program's fetch
controller pytests.
"""

from typing import List

# Email to authenticate a User to fetch programs.
FETCH_PROGRAMS_USER: str = "May.Parker@harris.com"

# Valid `Program` ids used to ensure the validity of our success case.
FETCH_PROGRAMS_ALL_VALID_IDS: List[int] = list(range(1, 1001))

# `Program` ids used for testing success case.
FETCH_PROGRAM_IDS: List[int] = [1, 2]

# Limit used in testing fetch `Program` with limit
# tests.
FETCH_PROGRAM_WITH_LIMIT: int = 2

# Valid `Program` id numbers expected for fetch with limit
# tests.
FETCH_PROGRAM_WITH_LIMIT_VALID_IDS: List[int] = [1, 2]

# Page number used in testing fetch `Program`
# with page tests.
FETCH_PROGRAM_WITH_PAGE: int = 1

# Ids used in testing fetch `Program` with page tests.
FETCH_PROGRAM_WITH_PAGE_IDS: List[int] = [i for i in range(1, 51)]

# Number of expected records within first page of `Programs`.
FETCH_PROGRAM_WITH_PAGE_EXPECTED_COUNT: int = 50

# Valid page and limit ids used for testing success case.
FETCH_PROGRAM_WITH_PAGE_AND_LIMIT_VALID_IDS: List[int] = [1, 2]

# Page number that exceeds the number of
# pages used in testing fetch `Program` with
# page tests.
FETCH_PROGRAM_WITH_PAGE_EXCEEDING_MAX_PAGE_COUNT: int = 99

# Number of programs expected after fetching `Program`s
# with a page number that exceeds the number of
# pages.
FETCH_PROGRAM_WITH_PAGE_EXCEEDING_MAX_PAGE_COUNT_RECORD_COUNT: int = 0

# Id used for testing fetch by `Program` id DNE tests.
FETCH_PROGRAM_BY_PROGRAM_ID_DNE: List[int] = [7880]

# Valid `Program` ids.
FETCH_PROGRAM_IDS_1: int = 1
FETCH_PROGRAM_IDS_2: int = 2

# Valid `Program` records.
EXPECTED_PROGRAMS_PROGRAM_ID_VALIDATE_PARAMS: dict = {
    FETCH_PROGRAM_IDS_1: {
        "id": 1,
        "segment": "SPACE & AIRBORNE SYSTEMS",
        "name": "Aegis AIN 987 Demo Ops_10LR #1",
        "created": "2025-03-08T06:37:32-05:00",
        "modified": "2024-05-01T12:19:00-04:00",
        "pa_number": "4X25J",
        "sector": "Air Defense",
        "division": "North Command",
        "tier": 2,
        "contract_type": "FFP",
        "contract_number": "CN841700",
        "contract_value": 606545312,
        "contract_start_date": "2025-01-01",
        "contract_end_date": "2025-12-01",
        "actual_cost_work_performed_cumulative": 70.36,
        "budgeted_cost_work_performed_cumulative": 20.55,
        "budgeted_cost_work_scheduled_cumulative": 59.46,
        "cost_performance_index_cumulative": 0.61,
        "schedule_performance_index_cumulative": 0.55,
        "budget_at_complete": 41.97,
        "estimate_at_complete": 84.95,
        "estimate_to_complete": 36.02,
        "management_reserve": 47.9,
        "weighted_risks_and_opportunities": 30.27,
        "active_status": True,
        "team_members": [],
    },
    FETCH_PROGRAM_IDS_2: {
        "id": 2,
        "segment": "SPACE & AIRBORNE SYSTEMS",
        "name": "Poseidon GIN 007 Demo Ops_10LR #2",
        "created": "2024-08-21T04:40:34-04:00",
        "modified": "2024-06-02T03:55:11-04:00",
        "pa_number": "4R010S",
        "sector": "Missile Systems",
        "division": "Tech Arm",
        "tier": 4,
        "contract_type": "FFP",
        "contract_number": "CN556010",
        "contract_value": 813759728,
        "contract_start_date": "2025-01-01",
        "contract_end_date": "2025-12-01",
        "actual_cost_work_performed_cumulative": 70.36,
        "budgeted_cost_work_performed_cumulative": 20.55,
        "budgeted_cost_work_scheduled_cumulative": 59.46,
        "cost_performance_index_cumulative": 0.97,
        "schedule_performance_index_cumulative": 1.43,
        "budget_at_complete": 41.97,
        "estimate_at_complete": 84.95,
        "estimate_to_complete": 36.02,
        "management_reserve": 47.9,
        "weighted_risks_and_opportunities": 30.27,
        "active_status": True,
        "team_members": [],
    },
}
