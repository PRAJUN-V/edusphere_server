from django.urls import path
from .views import RoomMessagesListView, RoomCreateView, RoomListView, RoomDeleteView

urlpatterns = [
    path('rooms/<int:room_id>/messages/', RoomMessagesListView.as_view(), name='room-messages-list'),
    path('rooms/create/', RoomCreateView.as_view(), name='room-create'),
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/delete/<int:id>/', RoomDeleteView.as_view(), name='room-delete'),
]
