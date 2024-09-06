from django.urls import path
from .consumers import ChatConsumer

# Use room_id instead of room_name
websocket_urlpatterns = [
    path("ws/messages/<int:room_id>/", ChatConsumer.as_asgi()),
]
