""" 
BI Portal `Analytics` view module. Views handle requests to process
additions/modifications/queries of BI Portal analytics. `Analytics`
provide insights into users' behaviors when using the application
that may help to improve the user experience or be of use to any
data science initiative.
"""

from .query.query import Query
from .visit.visit import Visit
