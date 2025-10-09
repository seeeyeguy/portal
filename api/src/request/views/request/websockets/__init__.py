from request.views import RequestNotification

from manager.websockets.consumers import APIConsumerFactory

get_consumer_factory = APIConsumerFactory(
    view_method="GET",
    view_handler=RequestNotification().get,
    group="request-notification",
    authentication_required=True,
)

GetRequestNotificationConsumer = get_consumer_factory.create_api_consumer()
