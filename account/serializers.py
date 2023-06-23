from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.serializers import ValidationError

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]

### 방금 붙인 코드 아래에 붙여주세요! ###

class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"
    
        def validate(self, attrs):
            username = attrs.get('username', '')
            password = attrs.get('password', '')
            email = attrs.get('email', '')
            if not (username and password and email):
                raise ValidationError({"detail": "[email, password, username] fields missing."})
            return attrs

class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
