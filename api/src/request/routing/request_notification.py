from django.urls import path

from request.views.request.websockets import GetRequestNotificationConsumer

urlpatterns = [
    path(
        route="ws/request-notification",
        view=GetRequestNotificationConsumer.as_asgi(),
        name="ws.request.request_notification",
    ),
]
