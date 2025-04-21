"""
`Request` Views module. Views permit the addition,
modification, fetching, and processing of data
through the Request/Response cycle. `Request`s
have a pivotal role within `BI Portal` as they
allow users to create, modify, and delete `Resource`s
through the request workflow. A `Resource` cannot be added,
modified, or deleted without proceeding through the request
workflow and receiving the needed approvals via a `Request`.
"""

from .request import Request
