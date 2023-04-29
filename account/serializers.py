from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from account.models import UserProfile
from rest_framework.serializers import ValidationError

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
    def validate(self, attrs): #attrs 대신 data도 가능
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        email = attrs.get('email', '')
        if not (username and password and email): #자료가 하나라도 없으면 validationerror가 돌아감
            raise ValidationError({"detail": "[email, password, username] fields missing."})
        return attrs


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True) 

    class Meta:
        model = UserProfile
        fields = "__all__"

class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]