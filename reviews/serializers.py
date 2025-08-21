from rest_framework import serializers
from .models import Review
from jobstatus.serializers import JobStatusSerializer

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source="reviewer.fullname", read_only=True)
    reviewer_pic = serializers.CharField(source="reviewer.profilepic", read_only=True)
    job=JobStatusSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ["job", "reviewer", "reviewee_user", "created_at"]
