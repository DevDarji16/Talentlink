# models.py
from django.db import models
from django.contrib.auth.models import User

class Canvas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='canvas')
    title = models.CharField(max_length=100, default="Untitled Canvas")
    data = models.JSONField(blank=True, null=True)  # Stores all Excalidraw elements
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    