"""
URLpatterns provides endpoints as a gateway between the server and
the client, where they can interact with the `Analytics` API, participating
in the request/response cycle.
"""

from django.urls import path

from analytics import views

from manager.utils.types import urlconfig

urlpatterns: urlconfig.PathPatternList = [
    path("queries", view=views.Query.as_view(), name="analytics.query"),
    path("visits", view=views.Visit.as_view(), name="analytics.visit"),
]
