from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/gamesession/', consumers.GameSessionConsumer.as_asgi())
]