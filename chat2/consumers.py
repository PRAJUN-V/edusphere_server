import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"room_{self.room_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.close(code)

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        event = {"type": "send_message", "message": data_json}

        await self.channel_layer.group_send(self.room_group_name, event)

    async def send_message(self, event):
        data = event["message"]

        # Create message in the database
        await self.create_message(data=data)

        # Fetch sender name
        sender_name = await self.get_sender_name(sender_id=data["sender_id"])

        # Send message to WebSocket
        response = {
            "sender_id": data["sender_id"],
            "sender_name": sender_name,  # Include sender_name
            "message": data["message"]
        }
        await self.send(text_data=json.dumps({"message": response}))

    @database_sync_to_async
    def create_message(self, data):
        try:
            room = Room.objects.get(id=self.room_id)
            sender = User.objects.get(id=data["sender_id"])

            if not Message.objects.filter(message=data["message"], sender=sender).exists():
                Message.objects.create(room=room, message=data["message"], sender=sender)
        except Room.DoesNotExist:
            print(f"Room with id {self.room_id} does not exist.")
        except User.DoesNotExist:
            print(f"User with id {data['sender_id']} does not exist.")

    @database_sync_to_async
    def get_sender_name(self, sender_id):
        try:
            sender = User.objects.get(id=sender_id)
            return sender.username  # or any other field you use for names
        except User.DoesNotExist:
            return "Unknown"
