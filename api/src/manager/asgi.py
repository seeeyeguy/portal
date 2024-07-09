"""
ASGI config for manager project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import importlib
import os
from typing import List

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from manager.settings import CUSTOM_APPS

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manager.settings")


def load_routing_modules_for_websockets(apps: List[str]) -> list:
    """Returns a list of websocket urlpatterns, given a list of
    installed Django Apps. Each app must have a `routing` module
    with an `__init__.py`. Each `__init__.py` must have a urlpatterns
    variable that contains all websocket routes for that app."""

    routes: list = []
    for app in apps:
        full_package_name = f"{app}.routing"
        try:
            module = importlib.import_module(full_package_name)
            routes.extend(module.urlpatterns)
        except (AttributeError, ModuleNotFoundError):
            pass  # fail silently
    return routes


django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(routes=load_routing_modules_for_websockets(apps=CUSTOM_APPS))
            )
        ),
    }
)
