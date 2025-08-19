# messaging/models.py
from django.db import models
from users.models import UserProfile

class Conversation(models.Model):
    participants = models.ManyToManyField(UserProfile, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        users = ", ".join([p.username for p in self.participants.all()])
        return f"Conversation: {users}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"
