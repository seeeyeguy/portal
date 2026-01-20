"""
Arguments to be shared for Task's create
controller pytests.
"""

from datetime import date

CREATE_TASK_USER_EMAIL: str = "May.Parker@harris.com"
CREATE_TASK_OWNER_EMAIL: str = "Peter.Parker@l3harris.com"

CREATE_TASK_PA_NUMBER: str = "489AB"
CREATE_TASK_REPORTING_PERIOD: int = 202502
CREATE_TASK_NAME: str = "Task New"
CREATE_TASK_DESCRIPTION: str = "New task description for unit testing."
CREATE_TASK_STATUS: str = "Not Started"
CREATE_TASK_ORDER: int = 1
CREATE_TASK_CREATE_DATE: date = date(2025, 1, 1)
CREATE_TASK_TARGET_DATE: date = date(2025, 1, 10)

CREATE_TASK_PREVIOUS_REVISION: int = 5
CREATE_TASK_PREVIOUS_REVISION_DNE: int = 99999999
CREATE_TASK_PA_NUMBER_DNE: str = "123ABC"

CREATE_TASK_EXPECTED_RESPONSE: dict = {
    "id": 6,
    "name": CREATE_TASK_NAME,
    "description": CREATE_TASK_DESCRIPTION,
    "status": CREATE_TASK_STATUS,
    "order": CREATE_TASK_ORDER,
    "owner": CREATE_TASK_OWNER_EMAIL,
    "pa_number": CREATE_TASK_PA_NUMBER,
    "reporting_period": [CREATE_TASK_REPORTING_PERIOD],
    "create_date": "2025-01-01",
    "target_date": "2025-01-10",
    "complete_date": None,
    "archive_date": None,
}

CREATE_TASK_PREVIOUS_REVISION_EXPECTED_RESPONSE: dict = {
    "id": 7,
    "name": CREATE_TASK_NAME,
    "description": CREATE_TASK_DESCRIPTION,
    "status": CREATE_TASK_STATUS,
    "order": CREATE_TASK_ORDER,
    "owner": CREATE_TASK_OWNER_EMAIL,
    "pa_number": CREATE_TASK_PA_NUMBER,
    "reporting_period": [CREATE_TASK_REPORTING_PERIOD],
    "create_date": "2025-01-01",
    "target_date": "2025-01-10",
    "complete_date": None,
    "archive_date": None,
}
