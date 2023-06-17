from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from account.models import UserProfile

##UserProfile 쓰려고 import 했음.
##. 은 '이 디렉토리 안에 있는' 이라는 뜻.
from rest_framework.serializers import ValidationError


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
        ## field 안에는 어떤 내용을 데이터로 변환할 건지를 적어준다.
        ## 지난번에는 fields = "__all__" 이렇게 적어줬는데, 장고에서 미리 만들어둔 유저 테이블에는 여러 칼럼이 있어서 all 하면 넘 많음.

    # def validate(self, attrs):
    #     username = attrs.get("username", "")
    #     password = attrs.get("password", "")
    #     email = attrs.get("email", "")
    #     if not (username and password and email):
    #         raise ValidationError(
    #             {"detail": "[email, password, username] fields missing."}
    #         )
    #     return attrs

    ##attrs -> data라는 뜻


class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"
