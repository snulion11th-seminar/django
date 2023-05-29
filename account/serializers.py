from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from account.models import UserProfile
from rest_framework.serializers import ValidationError

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
        
    # def validate(self, data):
    #     username = data.get('username', '')
    #     password = data.get('password', '')
    #     email = data.get('email', '')
    #     if not (username and password and email):
    #         raise ValidationError({"detail": "[email, password, username] fields missing."})
    #     return data


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]