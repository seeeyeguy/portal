from request.views import Disposition

from manager.websockets.consumers import APIConsumerFactory

post_consumer_factory = APIConsumerFactory(
    view_method="POST",
    view_handler=Disposition().post,
    group="disposition",
    authentication_required=True,
)

PostDispositionConsumer = post_consumer_factory.create_api_consumer()
