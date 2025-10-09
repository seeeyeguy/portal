from .disposition import urlpatterns as disposition_urlpatterns
from .request_notification import urlpatterns as request_notification_urlpatterns


urlpatterns = [*disposition_urlpatterns, *request_notification_urlpatterns]
