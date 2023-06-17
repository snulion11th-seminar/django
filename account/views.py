from django.shortcuts import render

# 회원가입 API 만들기
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserIdUsernameSerializer

#### 2
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def generate_token_in_serialized_data(
    user: User, user_profile: UserProfile
) -> UserSerializer.data:
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token)
    serialized_data = UserProfileSerializer(user_profile).data
    serialized_data["token"] = {"access": access_token, "refresh": refresh_token}
    return serialized_data


## 반복 코드 작업 방지용.. 재사용성 강화
def set_token_on_response_cookie(user: User) -> Response:
    token = RefreshToken.for_user(user)
    user_profile = UserProfile.objects.get(user=user)
    user_profile_serializer = UserProfileSerializer(user_profile)
    res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
    res.set_cookie("refresh_token", value=str(token))
    res.set_cookie("access_token", value=str(token.access_token))
    return res


#### view
class SignupView(APIView):
    def post(self, request):
        college = request.data.get("college")
        major = request.data.get("major")

        #### 3
        user_serializer = UserSerializer(data=request.data)
        ### 여태까지는 data = 이렇게 하지 않았고, object를 create해서 바로 serializing 해줬음.
        ### 이거는 request 에서 data에서 갖고 올 때는 object 형식이 아니라 Raw 한 데이터이기 때문에 data = 이렇게 해줘야함.
        if user_serializer.is_valid(raise_exception=True):
            ##
            user = user_serializer.save()

        user_profile = UserProfile.objects.create(
            user=user, college=college, major=major
        )

        return set_token_on_response_cookie(user)

        #### 4 return 때문에 밑에 있는 애들이 사라짐.
        serialized_data = generate_token_in_serialized_data(user, user_profile)

        return Response(serialized_data, status=status.HTTP_201_CREATED)


class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data["username"], password=request.data["password"]
            )
        except:
            return Response(
                {"detail": "아이디 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST
            )
        return set_token_on_response_cookie(user)


class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED
            )
        RefreshToken(request.data["refresh"]).blacklist()
        ### body 안에 있는 data
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenReissueView(APIView):
    def post(self, request):
        user = User.objects.get(username=request.data["username"])
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED
            )
        RefreshToken(request.data["refresh"]).blacklist()
        return Response({"access"})


class TokenReissueView(APIView):
    def post(self, request):
        user = User.objects.get(username=request.data["username"])
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED
            )
        refresh_token = RefreshToken(request.data["refresh"])
        refresh_token.blacklist()
        new_access_token = str(refresh_token.access_token)
        return Response({"access": new_access_token})


class UserInfoView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED
            )
        user = request.user
        serializer = UserIdUsernameSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED
            )
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED
            )
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED
            )

        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(
            user_profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
