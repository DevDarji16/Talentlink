from rest_framework import serializers
from .models import TalentLinkReview

class TalentLinkReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentLinkReview
        fields = ['id', 'name', 'comment', 'created_at']
