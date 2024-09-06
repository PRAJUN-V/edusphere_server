from rest_framework import serializers
from chat.models import Chatroom, Chat

class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'course']


# class ChatSerializer(serializers.ModelSerializer):
#     sender = serializers.StringRelatedField()  # This shows the string representation of the sender
#     sender_id = serializers.PrimaryKeyRelatedField(source='sender', read_only=True)  # This adds the sender's ID
#
#     class Meta:
#         model = Chat
#         fields = ['id', 'sender', 'sender_id', 'message', 'date']
#
#
# class RoomSerializer(serializers.ModelSerializer):
#     chats = ChatSerializer(many=True, read_only=True)  # Nested serializer for chats
#
#     class Meta:
#         model = Chatroom
#         fields = ['id', 'course', 'name', 'created_at', 'chats']
