from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["major", "college"] 
        
class UserSerializer(ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["username", "password", "email", "profile"]

class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]