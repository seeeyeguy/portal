"""
URLpatterns provides endpoints as a gateway between the server and
the client, where they can interact with the `Program Review Tool` API,
participating in the request/response cycle.
"""

from django.urls import path, re_path

from program_review_tool import views

from manager.utils.types import urlconfig

urlpatterns: urlconfig.PathPatternList = [
    re_path(
        r"program(\/review)?",
        view=views.Program.as_view(),
        name="program_review_tool.program",
    ),
    path(
        "portfolio",
        view=views.Portfolio.as_view(),
        name="program_review_tool.portfolio",
    ),
    path(
        "record",
        view=views.Record.as_view(),
        name="program_review_tool.record",
    ),
    path(
        "reporting-period",
        view=views.ReportingPeriod.as_view(),
        name="program_review_tool.reporting_period",
    ),
]
