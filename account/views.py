# accounts/views.py
from django.contrib.auth.models import User 
from django.contrib import auth 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from .serializers import UserSerializer,UserProfileSerializer, UserIdUsernameSerializer
from .models import UserProfile

def set_token_on_response_cookie(user:User) -> Response:
    token = RefreshToken.for_user(user)
    user_profile = UserProfile.objects.get(user=user)
    user_profile_serializer = UserProfileSerializer(user_profile)
    res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
    res.set_cookie('refresh_token', value=str(token))
    res.set_cookie('access_token', value=str(token.access_token))
    return res



class SignupView(APIView):
    def post(self, request):
        college=request.data.get('college')
        major=request.data.get('major')

        user_serialier = UserSerializer(data=request.data)
        if user_serialier.is_valid(raise_exception=True):
            user = user_serialier.save()
            
        user_profile = UserProfile.objects.create(
            user=user,
            college=college,
            major=major
        ) 
        return set_token_on_response_cookie(user)
        
class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
        except:
            return Response({"detail": "아이디 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        return set_token_on_response_cookie(user)
        
class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)      
        
class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data['refresh']
        try:
            RefreshToken(refresh_token).verify()
        except:
            return Response({"detail" : "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        new_access_token = str(RefreshToken(refresh_token).access_token)
        response = Response({"detail": "token refreshed"}, status=status.HTTP_200_OK)
        response.set_cookie('access_token', value=str(new_access_token))
        return response
    
class UserInfoView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        serializer = UserIdUsernameSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if not user_serializer.is_valid(raise_exception=True):
            return Response({"detail": "user data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()
        profile = UserProfile.objects.get(user=user)
        user_profile_serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if not user_profile_serializer.is_valid(raise_exception=True):
            return Response({"detail": "profile data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        user_profile_serializer.save()
        return Response(user_profile_serializer.data, status=status.HTTP_200_OK)