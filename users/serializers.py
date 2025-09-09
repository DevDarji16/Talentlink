from rest_framework import serializers
from .models import UserProfile,Gig, Job,Application,FreelanceGroup,Notification,GroupInvite
from allauth.socialaccount.models import SocialAccount
import uuid

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
        extra_kwargs = {
            'freelancer': {'read_only': True}
        }
        depth = 1 

class JobSerializer(serializers.ModelSerializer):
    client = UserProfileSerializer(read_only=True)
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['client', 'created_at']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['freelancer', 'client', 'status', 'created_at']

class ApplicationDetailSerializer(serializers.ModelSerializer):
    freelancer = UserProfileSerializer()
    client = UserProfileSerializer()
    job = JobSerializer()

    class Meta:
        model = Application
        fields = '__all__'

class FreelanceGroupSerializer(serializers.ModelSerializer):
    leader=UserProfileSerializer(read_only=True)
    members=UserProfileSerializer(read_only=True,many=True)
    class Meta:
        model=FreelanceGroup
        fields='__all__'
        read_only_fields = ['leader']


class GroupInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInvite
        fields = ['id', 'sender', 'receiver', 'group', 'status', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'type',
            'message',
            'is_read',
            'created_at',
            'related_group',
            'related_invite'
        ]

