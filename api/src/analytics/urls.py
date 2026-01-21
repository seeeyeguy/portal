"""
URLpatterns provides endpoints as a gateway between the server and
the client, where they can interact with the `Analytics` API, participating
in the request/response cycle.
"""

from django.urls import path

from analytics import views


urlpatterns = [
    path("queries", views.Query.as_view(), name="analytics.query"),
    path("visits", views.Visit.as_view(), name="analytics.visit"),
    path("favorites", views.FavoriteView.as_view(), name="analytics.favorites"),
    path("prt/usage", views.UsageView.as_view(), name="analytics.prt.usage"),
]
