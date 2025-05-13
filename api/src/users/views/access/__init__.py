"""
`Access` Views module. Views permit the addition,
modification, fetching, and processing of data
through the Request/Response cycle. `Access`es
have a critical role in `BI Portal`'s role-based
authorization, conveying permissions to a user
dependent on their role. More specifically, an
`Access` determines whether a user may submit a
request and/or disposition for the appropriate
subfunctions and stages in the `BI Portal` request
workflow.
"""

from .access import Access
