from rest_framework import serializers
from .models import GigApplication

class GigApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GigApplication
        fields = '__all__'
        read_only_fields = [
            'id',
            'status',
            'created_at'
        ]  