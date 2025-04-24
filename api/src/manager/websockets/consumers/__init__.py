"""
Consumer factory module. APIConsumerFactory provides functionality
to easily implement a view with websockets to allow for real time
communication between the client and the server. Instantiate an
instance of APIConsumerFactory with key data about the view and
then, use `APIConsumerFactory.create_api_consumer` to create an
instance of a JsonWebsocketConsumer that may process requests to
your view using websockets.
Ex. APIConsumerFactory("GET", my_view, "group_name").create_api_consumer().as_asgi()
"""

import json
import urllib.parse
from typing import Callable

from asgiref.sync import async_to_sync
from channels.exceptions import DenyConnection
from channels.generic.websocket import JsonWebsocketConsumer
from django import http
from django.contrib.auth import models

from manager.websockets.exceptions import APIConsumerFactoryConfigError


class APIConsumerFactory:
    """API Consumer Factory accepts several parameters that may be used to
    create a websocket `Consumer`. We can use these consumers as view
    functions for our websocket endpoints, executing the view handler
    passed to the factory's __init__ on each request.

    The init accepts:
        * view_method (GET|POST|PUT|DELETE): The method the view handler accepts.
        * view_handler (function): The function that will execute the business logic
            on each request. It must accept a Django.http.HttpRequest and
            return Django.http.JsonResponse.
        * group (str): The name of the channel group. Each `Consumer` within this group
            will receive the same response from the view handler whenever it is called.
        * authentication_required (bool): Is the user required to be authenticated to
            complete the request. If so, any request from an unauthenticated user will
            be rejected.
    """

    def __init__(
        self,
        view_method: str,
        view_handler: Callable,
        group: str,
        authentication_required: bool = False,
    ) -> None:
        if view_method not in ("GET", "POST", "PUT", "DELETE"):
            raise APIConsumerFactoryConfigError(f"Method({view_method}) not allowed!")

        self.method = view_method
        self.view = view_handler
        self.group = f"asgi_api_{group}"
        self.authentication_required = authentication_required

    def create_api_consumer(self) -> JsonWebsocketConsumer:
        """Create a websocket `Consumer` with the settings initialized
        in the factory's __init__."""

        factory = self

        class Consumer(JsonWebsocketConsumer):
            """Variant of WebsocketConsumer that automatically JSON-encodes and decodes
            messages as they come in and go out. Expects everything to be text;
            will error on binary data."""

            def connect(self) -> None:
                """Connect to a websocket."""

                # Pull the user from the scope.
                # pylint: disable=attribute-defined-outside-init
                self.user: models.User = self.scope["user"]
                # If authentication is required and the user is not logged in,
                # raise an error to reject the request.
                if factory.authentication_required and not self.user.is_authenticated:
                    raise DenyConnection("User must be authenticated.")

                # Add this consumer to the group.
                async_to_sync(self.channel_layer.group_add)(
                    factory.group, self.channel_name
                )
                # Accept the connection, using the default protocol.
                self.accept()

            def disconnect(self, _) -> None:  # type: ignore[no-untyped-def]
                """Leave consumer group and close
                connection to websocket."""

                # Leave group and close connection.
                async_to_sync(self.channel_layer.group_discard)(
                    factory.group, self.channel_name
                )

            def receive_json(self, content: dict, **kwargs: dict) -> None:
                """
                Process content of request sent by client, and
                relay that request to the factory's view handler.

                Accepts:
                    * content (dict): Data sent by the client.

                Returns:
                    * None
                """

                # Create a request to relay to view handler.
                request = http.HttpRequest()
                request.headers = self.scope["headers"]
                request.method = factory.method
                request.path = self.scope["path"]
                setattr(request, "url_route", self.scope["url_route"])
                setattr(request, "user", self.user)

                if factory.method == "GET":
                    # If request is GET, initialize query params.
                    query_params = http.QueryDict(
                        urllib.parse.urlencode(content), mutable=False
                    )
                    request.GET = query_params
                else:
                    # Otherwise, put the data in the body of the request.
                    body = json.dumps(content)
                    request.content_type = "application/json"
                    # pylint: disable=protected-access
                    request._body = body  # type: ignore[assignment]

                # Send the request to the view for processing.
                response: http.JsonResponse = factory.view(request)

                # Send response content & status code to channel group.
                async_to_sync(self.channel_layer.group_send)(
                    factory.group,
                    {
                        "type": "send.response.to.group",
                        "content": json.loads(response.content),
                        "status": response.status_code,
                    },
                )

            def send_response_to_group(self, event: dict) -> None:
                """
                Process event initiated by the consumer. Send response to
                all members of the group.

                Accept:
                    * event (dict): Data sent to members of group.

                Returns:
                    * None
                """

                # Send response content & status to client(s).
                self.send_json({"content": event["content"], "status": event["status"]})

        return Consumer
