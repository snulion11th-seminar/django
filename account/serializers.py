from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.serializers import ValidationError
from rest_framework import serializers
class UserSerializer(ModelSerializer):
    username=serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

        def validate(self, attrs):
            print("hihi")
            username = attrs.get('username', '')
            password = attrs.get('password')
            email = attrs.get('email', '')
            if not (username and password and email):
                raise ValidationError({"detail": "[email, password, username] fields missing."})
            return attrs

class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"