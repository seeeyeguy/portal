"""
`BI Portal` `Request` controller module. Controllers create,
fetch, and update records within the `Request` table. `Request`
represent a request by a `User` to create, update, or delete
a `Resource` record within `BI Portal`. A `Resource` record
must be related to a `Request` that has been processed through
the `BI Portal` request workflow with the needed approvals
before any change can be made in `BI Portal`'s published
`Resource` record dataset.
"""
