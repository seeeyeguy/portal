"""
Arguments to be shared for Task's update
controller pytests.
"""

from datetime import date

UPDATE_TASK_USER_EMAIL: str = "May.Parker@harris.com"
UPDATE_TASK_OWNER_EMAIL: str = "Peter.Parker@harris.com"
UPDATE_TASK_TASK_ID: int = 4
UPDATE_TASK_PA_NUMBER: str = "489AB"
UPDATE_TASK_REPORTING_PERIOD: int = 202502
UPDATE_TASK_NAME: str = "Task New"
UPDATE_TASK_DESCRIPTION: str = "New task description for unit testing."
UPDATE_TASK_STATUS: str = "Done and Archived"
UPDATE_TASK_ORDER: int = 10
UPDATE_TASK_CREATE_DATE: date = date(2025, 1, 1)
UPDATE_TASK_TARGET_DATE: date = date(2026, 1, 1)
UPDATE_TASK_COMPLETE_DATE: date = date(2026, 1, 1)
UPDATE_TASK_ARCHIVE_DATE: date = date(2026, 1, 10)

UPDATE_TASK_TASK_ID_DNE: int = 999999
UPDATE_TASK_TASK_ID_MULTIPLE_REPORTING_PERIODS: int = 5
UPDATE_TASK_PA_NUMBER_WRONG_PA_NUMBER: str = "123ABC"
UPDATE_TASK_REPORTING_PERIOD_WRONG_REPORTING_PERIOD: int = 202503

UPDATE_TASK_EXPECTED_RESPONSE: dict = {
    "id": UPDATE_TASK_TASK_ID,
    "previous_revision": None,
    "name": UPDATE_TASK_NAME,
    "description": UPDATE_TASK_DESCRIPTION,
    "status": UPDATE_TASK_STATUS,
    "order": UPDATE_TASK_ORDER,
    "owner": UPDATE_TASK_OWNER_EMAIL,
    "pa_number": UPDATE_TASK_PA_NUMBER,
    "reporting_period": [UPDATE_TASK_REPORTING_PERIOD],
    "create_date": "2025-01-01",
    "target_date": "2026-01-01",
    "complete_date": "2026-01-01",
    "archive_date": "2026-01-10",
}

UPDATE_TASK_EXPECTED_ROWS_AFFECTED = 1

############### ADD REPORTING PERIOD TEST DATA ########################

ADD_REPORTING_PERIOD_PERIOD: int = 202503

ADD_REPORTING_PERIOD_EXPECTED_RESPONSE: dict = {
    "id": UPDATE_TASK_TASK_ID,
    "previous_revision": None,
    "name": "Task Gamma",
    "description": "Develop prototype and conduct preliminary testing.",
    "status": "Pending Review",
    "order": 2,
    "owner": "Peter.Parker@harris.com",
    "pa_number": UPDATE_TASK_PA_NUMBER,
    "reporting_period": [UPDATE_TASK_REPORTING_PERIOD, ADD_REPORTING_PERIOD_PERIOD],
    "create_date": "2025-01-01",
    "target_date": "2025-05-01",
    "complete_date": None,
    "archive_date": None,
}

################ REMOVE REPORTING PERIOD TEST DATA ######################

REMOVE_REPORTING_PERIOD_PERIOD: int = 202502

REMOVE_REPORTING_PERIOD_EXPECTED_RESPONSE: dict = {
    "id": UPDATE_TASK_TASK_ID,
    "previous_revision": None,
    "name": "Task Gamma",
    "description": "Develop prototype and conduct preliminary testing.",
    "status": "Pending Review",
    "order": 2,
    "owner": "Peter.Parker@harris.com",
    "pa_number": UPDATE_TASK_PA_NUMBER,
    "reporting_period": [],
    "create_date": "2025-01-01",
    "target_date": "2025-05-01",
    "complete_date": None,
    "archive_date": None,
}
