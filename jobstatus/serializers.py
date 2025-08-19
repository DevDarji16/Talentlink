from rest_framework import serializers
from .models import JobStatus
from users.serializers import UserProfileSerializer,GigSerializer,ApplicationDetailSerializer,FreelanceGroupSerializer
from draft.serializers import DraftSerializer

class JobStatusSerializer(serializers.ModelSerializer):
    client = UserProfileSerializer(read_only=True)
    freelancer = UserProfileSerializer(read_only=True)
    gig = GigSerializer(read_only=True)
    job = ApplicationDetailSerializer(read_only=True)
    draft = DraftSerializer(read_only=True)

    class Meta:
        model = JobStatus
        fields = '__all__'