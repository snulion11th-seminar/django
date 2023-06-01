from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "id"]

class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = "__all__"
        

class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
