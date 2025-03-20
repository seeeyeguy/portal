from django.urls import path

from request.views.disposition.websockets import PostDispositionConsumer

urlpatterns = [
    path(
        route="ws/disposition",
        view=PostDispositionConsumer.as_asgi(),
        name="ws.request.disposition",
    ),
]
