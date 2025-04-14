"""
Arguments to be shared for Portfolio's fetch
controller pytests.
"""

FETCH_PORTFOLIO_USER_EMAIL: str = "May.Parker@harris.com"

EXPECTED_PORTFOLIOS = [
    {
        "id": 1,
        "name": "Portfolio Name 1",
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
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "pa_number": "6C27",
                "sector": "Airborne Combat Systems",
                "division": "Electronic Warfare",
                "tier": 1,
                "contract_value": 3000000000,
                "active_status": True,
            },
            {
                "id": 2,
                "segment": "SPACE & AIRBORNE SYSTEMS",
                "name": "Zeus CLIN 0005 Single Launch_10LR",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "pa_number": "10LR",
                "sector": "Space Systems",
                "division": "Surveillance Systems",
                "tier": 3,
                "contract_value": 3000000000,
                "active_status": True,
            },
        ],
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
    },
    {
        "id": 2,
        "name": "Portfolio Name 2",
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
                "id": 3,
                "segment": "SPACE & AIRBORNE SYSTEMS",
                "name": "Zeus CLIN 0006 Demo and Ops_10MR",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "pa_number": "10MR",
                "sector": "Space Systems",
                "division": "Surveillance Systems",
                "tier": 4,
                "contract_value": 3000000000,
                "active_status": True,
            },
            {
                "id": 4,
                "segment": "SPACE & AIRBORNE SYSTEMS",
                "name": "Zeus Critical Spares_61GK",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "pa_number": "61GK",
                "sector": "Space Systems",
                "division": "Surveillance Systems",
                "tier": 4,
                "contract_value": 3000000000,
                "active_status": True,
            },
        ],
        "created": "2024-08-27T12:00:00-04:00",
        "modified": "2024-08-27T12:00:00-04:00",
    },
]
