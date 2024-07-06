from django.urls import re_path
from .consumers import *
from . import consumers
from django.urls import path

websocket_urlpatterns = [
    re_path('ws/socket-server/(?P<room_name>\w+)/$',consumers.ChatConsumer.as_asgi()),
]