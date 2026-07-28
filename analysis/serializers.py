from rest_framework import serializers
from .models import Scan

class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ['id', 'user', 'image', 'vision_output', 'recommendation', 'created_at']
        read_only_fields = ['user', 'vision_output', 'recommendation', 'created_at']
        