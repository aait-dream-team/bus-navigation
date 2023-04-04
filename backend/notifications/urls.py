from django.urls import  re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'^ws/trip/notification/(?P<trip_name>[^/]+)/$', consumer.NotificationConsumer.as_asgi()),
]