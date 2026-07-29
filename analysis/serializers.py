from rest_framework import serializers
from .models import Scan
from django.contrib.auth.models import User


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ['id', 'user', 'image', 'vision_output', 'recommendation', 'created_at']
        read_only_fields = ['user', 'vision_output', 'recommendation', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user        
        