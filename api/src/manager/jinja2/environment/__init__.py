"""
Template environment module for Jinja2. Jinja2 is a
fast, expressive, extensible templating engine that
provides a more robust developer experience. It is the
preferred template engine when developing our applications,
but there are certain tags, filters, and functions that are
provided by the Django templating engine that would be useful
so we override Jinja2 default environment to include these
as needed.
"""

from typing import Any

from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment

# pylint: disable=invalid-name


def JinjaEnvironment(**options: Any) -> Environment:
    """Jinja template environment for loading
    and rendering templates."""

    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
        }
    )
    return env
