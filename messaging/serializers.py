# messaging/serializers.py
from rest_framework import serializers
from .models import Conversation, Message
from users.models import UserProfile
from users.serializers import UserProfileSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'text', 'created_at', 'is_read']
        read_only_fields = ['sender', 'created_at', 'is_read']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserProfileSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at']
