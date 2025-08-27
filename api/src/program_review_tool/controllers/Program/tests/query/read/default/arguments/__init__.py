"""
Arguments to be shared for Program's fetch
controller pytests.
"""

from typing import List

# Email to authenticate a User to fetch programs.
FETCH_PROGRAMS_USER: str = "May.Parker@harris.com"

# Email of `ProgramMember` `User` that does not exist.
FETCH_PROGRAMS_PROGRAM_MEMBER_USER_DNE_EMAIL: str = "User.DNE@harris.com"

# Valid `Program` ids used to ensure the validity of our success case.
FETCH_PROGRAMS_ALL_VALID_IDS: List[int] = list(range(1, 1001))

# `Program` ids used for testing success case.
FETCH_PROGRAM_IDS: List[int] = [1, 2]

# `Program` PA numbers used for testing success case.
FETCH_PROGRAM_PA_NUMBERS: List[str] = ["4X25J", "4R010S"]

# `Program` tiers used for testing success case.
FETCH_PROGRAMS_BY_TIERS_TIERS: List[int] = [4]

# Valid `Program` ids expected for fetching `Program`s by tiers
# tests.
FETCH_PROGRAMS_BY_TIERS_VALID_IDS: List[int] = [
    2,
    10,
    14,
    15,
    26,
    29,
    32,
    38,
    40,
    41,
    44,
    48,
    54,
    69,
    72,
    73,
    74,
    83,
    85,
    90,
    91,
    94,
    102,
    105,
    111,
    115,
    117,
    124,
    125,
    128,
    137,
    140,
    141,
    142,
    144,
    145,
    146,
    151,
    158,
    162,
    165,
    173,
    187,
    188,
    191,
    193,
    194,
    197,
    207,
    214,
    216,
    219,
    231,
    234,
    235,
    236,
    238,
    239,
    241,
    243,
    249,
    251,
    255,
    257,
    258,
    263,
    270,
    279,
    285,
    288,
    293,
    308,
    309,
    313,
    316,
    321,
    323,
    324,
    327,
    328,
    331,
    333,
    337,
    342,
    344,
    345,
    352,
    363,
    368,
    375,
    381,
    383,
    385,
    394,
    396,
    400,
    402,
    404,
    407,
    409,
    412,
    415,
    424,
    428,
    430,
    433,
    438,
    448,
    451,
    454,
    457,
    463,
    469,
    471,
    480,
    481,
    482,
    485,
    486,
    492,
    499,
    500,
    508,
    515,
    517,
    525,
    530,
    536,
    543,
    545,
    552,
    553,
    562,
    564,
    565,
    566,
    569,
    570,
    575,
    578,
    583,
    585,
    592,
    595,
    599,
    600,
    601,
    605,
    619,
    626,
    632,
    633,
    635,
    646,
    652,
    653,
    662,
    680,
    682,
    684,
    689,
    691,
    699,
    706,
    709,
    710,
    715,
    719,
    726,
    728,
    731,
    733,
    734,
    738,
    749,
    750,
    756,
    760,
    763,
    764,
    765,
    768,
    772,
    778,
    780,
    783,
    785,
    796,
    799,
    802,
    813,
    815,
    821,
    822,
    827,
    833,
    835,
    840,
    841,
    844,
    847,
    848,
    850,
    857,
    864,
    867,
    868,
    873,
    876,
    881,
    886,
    892,
    902,
    905,
    906,
    909,
    918,
    919,
    926,
    927,
    928,
    929,
    930,
    931,
    936,
    937,
    942,
    943,
    947,
    948,
    950,
    951,
    956,
    957,
    960,
    961,
    966,
    976,
    978,
    981,
    987,
    988,
    989,
    993,
    996,
    997,
    1000,
]

# `User` email used when testing fetch `Program`s by `ProgramMember`.
FETCH_PROGRAMS_BY_PROGRAM_MEMBER_USER_EMAIL: str = "Peter.Parker@harris.com"

# Valid `Program` ids expected for fetching `Program`s by `ProgramMember`
# tests.
FETCH_PROGRAMS_BY_PROGRAM_MEMBER_VALID_IDS: List[int] = [5, 7, 8, 9, 35, 46]

# `Program` tiers used when testing fetch `Program`s by tiers and `ProgramMember`.
FETCH_PROGRAMS_BY_TIERS_AND_PROGRAM_MEMBER_TIERS: List[int] = [2]

# Valid `Program` ids expected for fetching `Program`s by tiers and `ProgramMember`
# tests.
FETCH_PROGRAMS_BY_TIERS_AND_PROGRAM_MEMBER_VALID_IDS: List[int] = [5, 8, 35]

# `User` email used when testing fetch `Program`s by `ProgramMember` that does
# not have an active `ProgramMember` entry.
FETCH_PROGRAMS_BY_PROGRAM_MEMBER_NO_ACTIVE_PROGRAM_MEMBER_USER_EMAIL: str = (
    "Tony.Stark@harris.com"
)

# Number of `Program` records expected for fetching `Program`s by `ProgramMember`
# with an e-mail of a `User` that does not have an active `ProgramMember` entry.
FETCH_PROGRAMS_BY_PROGRAM_MEMBER_NO_ACTIVE_PROGRAM_MEMBER_PROGRAM_COUNT: int = 0

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

FETCH_PROGRAM_BY_PROGRAM_PA_NUMBER_DNE: List[str] = ["DNE_TEST"]

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
