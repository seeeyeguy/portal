"""
Arguments to be shared for Task's fetch
controller pytests.
"""

FETCH_TASKS_PA_NUMBER = "489AB"

FETCH_TASKS_EMPTY_PA_NUMBER = "123ABC"

FETCH_TASKS_PREVIOUS_PERIOD = 202501

FETCH_TASKS_CURRENT_PERIOD = 202502

FETCH_TASKS_FUTURE_PERIOD = 202503

FETCH_TASKS_PREVIOUS_EXPECTED_TASKS = [
    {
        "id": 2,
        "name": "Task Beta",
        "description": "Initial analysis of system requirements.",
        "status": "Not Started",
        "order": 1,
        "owner": "Peter.Parker@l3harris.com",
        "pa_number": "489AB",
        "reporting_period": [202501],
        "create_date": "2025-01-01",
        "target_date": "2025-10-01",
        "complete_date": None,
        "archive_date": None,
    },
    {
        "id": 5,
        "name": "Task Delta",
        "description": "Finalize design, documentation, and handover.",
        "status": "Not Started",
        "order": 3,
        "owner": "Peter.Parker@l3harris.com",
        "pa_number": "489AB",
        "reporting_period": [202501, 202502],
        "create_date": "2025-01-01",
        "target_date": "2025-10-01",
        "complete_date": None,
        "archive_date": None,
    },
    {
        "id": 1,
        "name": "Task Alpha",
        "description": "Beginning Planning.",
        "status": "Completed",
        "order": None,
        "owner": "Peter.Parker@l3harris.com",
        "pa_number": "489AB",
        "reporting_period": [202501, 202502],
        "create_date": "2024-01-01",
        "target_date": "2025-01-01",
        "complete_date": "2025-01-01",
        "archive_date": "2025-02-01",
    },
]

FETCH_TASKS_CURRENT_EXPECTED_TASKS = [
    {
        "id": 3,
        "name": "Task Beta",
        "description": "Initial analysis of system requirements.",
        "status": "In Progress",
        "order": 1,
        "owner": "Peter.Parker@l3harris.com",
        "pa_number": "489AB",
        "reporting_period": [202502],
        "create_date": "2025-01-01",
        "target_date": "2025-10-01",
        "complete_date": "2025-08-01",
        "archive_date": None,
    },
    {
        "id": 4,
        "name": "Task Gamma",
        "description": "Develop prototype and conduct preliminary testing.",
        "status": "Pending Review",
        "order": 2,
        "owner": "Peter.Parker@l3harris.com",
        "pa_number": "489AB",
        "reporting_period": [202502],
        "create_date": "2025-01-01",
        "target_date": "2025-05-01",
        "complete_date": None,
        "archive_date": None,
    },
    {
        "id": 5,
        "name": "Task Delta",
        "description": "Finalize design, documentation, and handover.",
        "status": "Not Started",
        "order": 3,
        "owner": "Peter.Parker@l3harris.com",
        "pa_number": "489AB",
        "reporting_period": [202501, 202502],
        "create_date": "2025-01-01",
        "target_date": "2025-10-01",
        "complete_date": None,
        "archive_date": None,
    },
    {
        "id": 1,
        "name": "Task Alpha",
        "description": "Beginning Planning.",
        "status": "Completed",
        "order": None,
        "owner": "Peter.Parker@l3harris.com",
        "pa_number": "489AB",
        "reporting_period": [202501, 202502],
        "create_date": "2024-01-01",
        "target_date": "2025-01-01",
        "complete_date": "2025-01-01",
        "archive_date": "2025-02-01",
    },
]
