"""
`Analytics` models module. Models conform to our data model and
provide access to Django migrations and ORM. These models help
to store and manage BI portal analytics. With these analytics,
we can provide a more customized user experience and perform
data analytics to gleam insights about resources.
"""

from analytics.models.Query import Query
from analytics.models.Visit import Visit
