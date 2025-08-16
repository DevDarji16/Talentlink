# serializers.py
from rest_framework import serializers
from .models import Canvas

class CanvasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canvas
        fields = ['id', 'title','data', 'created_at']