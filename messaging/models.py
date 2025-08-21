# messaging/models.py
from django.db import models
from users.models import UserProfile

class Conversation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # for group chats
    is_group = models.BooleanField(default=False)
    participants = models.ManyToManyField(UserProfile, related_name="conversations")
    last_message = models.TextField(blank=True, null=True)  # preview text
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        users = ", ".join([p.username for p in self.participants.all()])
        return f"Conversation: {users}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Read receipts
    is_read = models.BooleanField(default=False)  # global read (1-1 case)
    read_by = models.ManyToManyField(UserProfile, related_name="read_messages", blank=True)  # group case

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"