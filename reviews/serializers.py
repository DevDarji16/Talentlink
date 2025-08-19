from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source="reviewer.fullname", read_only=True)
    reviewer_pic = serializers.CharField(source="reviewer.profilepic", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "job", "reviewer", "reviewed_user", "rating", "comment", "created_at", "reviewer_name", "reviewer_pic"]
        read_only_fields = ["job", "reviewer", "reviewed_user", "created_at"]
