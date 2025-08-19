from rest_framework import serializers
from .models import GigApplication
from users.serializers import UserProfileSerializer,GigSerializer
from users.models import UserProfile

class GigApplicationSerializer(serializers.ModelSerializer):
    client = UserProfileSerializer(read_only=True)
    freelancer = UserProfileSerializer(read_only=True)
    gig = GigSerializer(read_only=True)

    class Meta:
        model = GigApplication
        fields = '__all__'
        read_only_fields = ['id', 'status', 'created_at', 'client', 'freelancer', 'gig']
