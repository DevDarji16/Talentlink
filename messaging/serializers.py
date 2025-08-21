# messaging/serializers.py
from rest_framework import serializers
from users.serializers import UserProfileSerializer
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)
    read_by = UserProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'text', 'created_at', 'is_read', 'read_by']
        read_only_fields = ['sender', 'created_at', 'is_read', 'read_by']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserProfileSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'last_message', 'updated_at']

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        return last_msg.text if last_msg else None