"""
URLpatterns provides endpoints as a gateway between the server and
the client, where they can interact with the `Preferences` API, participating
in the request/response cycle.
"""

from django.urls import path

from preferences import views

from manager.utils.types import urlconfig

urlpatterns: urlconfig.PathPatternList = [
    path(
        "favorites",
        view=views.Favorite.as_view(),
        name="preferences.favorite",
    ),
    path(
        "query-filter-state",
        view=views.QueryFilterState.as_view(),
        name="preferences.query-filter-state",
    ),
]
