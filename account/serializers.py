from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.serializers import ValidationError

## from .(data) 현재 디렉토리에서 가져오기

from account.models import UserProfile
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"] ##어떤 내용을 serialize 할 것인가? (columns)
        
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