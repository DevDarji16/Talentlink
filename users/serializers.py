from rest_framework import serializers
from .models import UserProfile
from allauth.socialaccount.models import SocialAccount

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields='__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=SocialAccount
        fields='__all__'