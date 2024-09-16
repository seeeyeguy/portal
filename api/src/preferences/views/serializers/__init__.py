"""
Serializers for requests to the `BI Portal` `Preferences` views module.
"""

from preferences.views.serializers.favorite import (
    CreateFavoriteRequest,
    RankFavoriteRequest,
    RankFavoriteQueryParams,
    DeleteFavoriteRequest,
    FetchFavoriteRequest,
)
from preferences.views.serializers.query_filter_state import (
    CreateQueryFilterStateRequest,
    UpdateQueryFilterStateRequest,
    UpdateQueryFilterStateQueryParams,
    FetchQueryFilterStateRequest,
)
