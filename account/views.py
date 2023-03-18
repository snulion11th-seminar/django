# accounts/views.py
from django.contrib.auth.models import User 
from django.contrib import auth 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from .serializers import UserSerializer,UserProfileSerializer
from .models import UserProfile

def generate_token_in_serialized_data(user:User) -> str:
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token)
    serialized_data = UserSerializer(user).data
    serialized_data['token']={"access":access_token, "refresh":refresh_token}
    return serialized_data

class SignupView(APIView):
    def post(self, request):
        email=request.data.get("email")
        username=request.data.get('username')
        password=request.data.get('password')
        college=request.data.get('college')
        major=request.data.get('major')
        if not email or not username or not password:
            return Response({"detail": "[email, password, username] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(username=username):
            return Response({"detail": "user already exists."}, status=status.HTTP_403_FORBIDDEN)
        user = User.objects.create(
            email=email,
            username=username,
            password=password
            )
        user_profile = UserProfile.objects.create(
            user=user,
            college=college,
            major=major
        )
        serialized_data = generate_token_in_serialized_data(user)
        return Response(serialized_data, status=status.HTTP_201_CREATED)
        
class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
        except:
            return Response({"detail": "아이디 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        serialized_data = generate_token_in_serialized_data(user)
        return Response(serialized_data, status=status.HTTP_200_OK)
        
class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class TokenRefreshView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        elif not RefreshToken(request.data['refresh']).verify():
            return Response({"detail": "refresh token 이 blacklist 에 있습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        token = AccessToken.for_user(user)
        access_token = str(token)
        return Response({"access": access_token}, status=status.HTTP_200_OK)
        
class ProfileUpdateView(APIView):
    def patch(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True) 
        if not serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)