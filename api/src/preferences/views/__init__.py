""" 
BI Portal `Preferences` view module. Views handle requests to process
additions/modifications/queries to favorites and preferred filters, with which
we promote an improved user experience as users can save their favorite
resources and preferred initial state of the application.
"""

from .favorite.favorite import Favorite
from .query_filter_state.query_filter_state import QueryFilterState
