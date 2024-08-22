"""
`EmployeeLevel` module. `EmployeeLevel` represents a strictly
defined set of filters associated with resources. As of
08/06/2024, `EmployeeLevel` is restricted to the values of
`EMPLOYEE`, `MANAGER`, and `EXECUTIVE`. These are used to
relate a `Resource` to a specific type of employee, thus users
may filter for resources related to their areas of concern.
"""

from directory.models.EmployeeLevel.EmployeeLevel import EmployeeLevel
