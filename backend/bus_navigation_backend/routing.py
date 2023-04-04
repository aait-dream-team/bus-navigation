
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from notifications.urls import websocket_urlpatterns as notifications_websocket_urlpatterns


websocket_urlpatterns = []

websocket_urlpatterns += notifications_websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})