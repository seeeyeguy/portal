"""
Serializers for requests to the `BI Portal` `Analytics` views module.
"""

from analytics.views.serializers.query import CreateQueryRequest, FetchQueryRequest
from analytics.views.serializers.visit import CreateVisitRequest, FetchVisitRequest
from analytics.views.serializers.favorite import FetchFavoritesRequest
from analytics.views.serializers.usage import FetchUsageRequest
