from rest_framework import serializers
from .models import UserProfile,Gig, Job
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


class GigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gig
        fields = '__all__'  
        read_only_fields = ['freelancer', 'created_at']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['client', 'created_at']