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
        "email": "May.Parker@harris.com",
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
            "contract_value": 1000000000,
            "active_status": True,
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
            "contract_value": 2000000000,
            "active_status": True,
        },
    ],
}
