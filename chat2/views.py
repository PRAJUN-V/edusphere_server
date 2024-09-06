from rest_framework import generics
from .models import Message, Room
from .serializers import MessageSerializer, RoomSerializer

class RoomMessagesListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return Message.objects.filter(room_id=room_id).order_by('id')

class RoomCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomDeleteView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    lookup_field = 'id'
