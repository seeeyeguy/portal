"""
Arguments to be shared for Portfolio's update
controller pytests.
"""

from typing import List

# Name of `Portfolio` user for a successful update.
UPDATE_PORTFOLIO_USER_EMAIL: str = "May.Parker@harris.com"

# Id of `Portfolio` used for a successful update.
UPDATE_PORTFOLIO_PORTFOLIO_ID: int = 1

# Name of `Portfolio` used for a successful update.
UPDATE_PORTFOLIO_PORTFOLIO_NAME: str = "Updated Portfolio Name 1"

# List of `Program` ids used for a successful update.
UPDATE_PORTFOLIO_PROGRAM_IDS: List[int] = [1, 2]

# Duplicate `Portfolio` id used for testing failure case.
UPDATE_PORTFOLIO_DUPLICATE_PORTFOLIO_NAME_FOR_USER_PORTFOLIO_ID: int = 2

# Duplicate `Portfolio` name used for testing failure case.
UPDATE_PORTFOLIO_DUPLICATE_PORTFOLIO_NAME_FOR_USER: str = "Existing Portfolio Name"

# DNE `Portfolio` id used for testing failure case.
UPDATE_PORTFOLIO_PORTFOLIO_ID_DNE: int = 5

# DNE `Program` ids used for testing failure case.
UPDATE_PORTFOLIO_PROGRAM_IDS_DNE: List[int] = [9998, 9999]

# Number of expected `Portfolio` records to be affected after a
# successful update.
UPDATE_PORTFOLIO_EXPECTED_ROWS_AFFECTED: int = 1

UPDATE_PORTFOLIO_EXPECTED_PORTFOLIO: dict = {
    "id": 1,
    "name": "Updated Portfolio Name 1",
    "user": {
        "id": 1,
        "username": "May.Parker@harris.com",
        "email": "May.Parker@harris.com",
        "first_name": "May",
        "last_name": "Parker",
        "is_active": True,
    },
    "programs": [
        {
            "id": 1,
            "segment": "SPACE & AIRBORNE SYSTEMS",
            "name": "Aegis AIN 987 Demo Ops_10LR #1",
            "created": "2025-03-08T06:37:32-05:00",
            "modified": "2024-05-01T12:19:00-04:00",
            "pa_number": "4X25J",
            "sector": "Air Defense",
            "division": "North Command",
            "tier": 2,
            "contract_value": 606545312,
            "active_status": True,
        },
        {
            "id": 2,
            "segment": "SPACE & AIRBORNE SYSTEMS",
            "name": "Poseidon GIN 007 Demo Ops_10LR #2",
            "created": "2024-08-21T04:40:34-04:00",
            "modified": "2024-06-02T03:55:11-04:00",
            "pa_number": "4R010S",
            "sector": "Missile Systems",
            "division": "Tech Arm",
            "tier": 4,
            "contract_value": 813759728,
            "active_status": True,
        },
    ],
}
