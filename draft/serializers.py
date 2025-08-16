# draft/serializers.py
from rest_framework import serializers
from .models import Draft
from users.serializers import UserProfileSerializer, FreelanceGroupSerializer

class DraftSerializer(serializers.ModelSerializer):
    # Show user-friendly data instead of raw IDs
    freelancer = UserProfileSerializer(read_only=True)
    client = UserProfileSerializer(read_only=True)
    group = FreelanceGroupSerializer(read_only=True, allow_null=True)
    
    class Meta:
        model = Draft
        fields = [
            'id',
            'title',
            'description',
            'price',
            'freelancer',
            'client',
            'group',
            'created_at',
            'is_accepted'
        ]
        read_only_fields = ['freelancer', 'is_accepted']  # Set by server