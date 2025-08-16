from rest_framework import serializers
from .models import JobStatus

class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobStatus
        fields = [
            'id',
            'status',
            'created_at',
            'client',
            'freelancer',
            'group',
            'job',
            'gig',
            'draft'
        ]