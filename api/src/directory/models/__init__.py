"""
`Directory` models module. Models conform to our data model and
provide access to Django migrations and ORM. These models help
store and manage BI portal directory resources and their supporting
entities, including `Function`, `SubFunction`, `EmployeeLevel`, and `Tag`.
Resources are the links to external applications that a user may navigate
to. `Function`s, `SubFunction`s, `EmployeeLevel`s, and `Tag`s are supporting
entities that are use to catalog, classify, and group resources, making
them easier to find and manage. These models provide the primary
functionality of the application, enabling users to easily find and
navigate to the internal applications/tools offered by various departments
within L3harris Technologies.
"""

from directory.models.EmployeeLevel import EmployeeLevel
from directory.models.Function import Function
from directory.models.SubFunction import SubFunction
from directory.models.Tag import Tag
from directory.models.Resource import Resource, thumbnail_path
from directory.models.Resource.PointOfContact import PointOfContact
