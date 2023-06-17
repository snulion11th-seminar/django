from django.shortcuts import render
from seminar.settings import SECRET_KEY

# Create your views here.
import jwt

#### 1
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer,UserProfileSerializer, UserIdUsernameSerializer
#### 2
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def generate_token_in_serialized_data(user:User, user_profile:UserProfile) -> UserSerializer.data:
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token)
    serialized_data = UserProfileSerializer(user_profile).data
    serialized_data['token']={"access":access_token, "refresh":refresh_token}
    return serialized_data

def set_token_on_response_cookie(user: User, user_profile: UserProfile) -> Response:
    token = RefreshToken.for_user(user)
    user_profile = UserProfile.objects.get(user=user)
    user_profile_serializer = UserProfileSerializer(user_profile)
    res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
    res.set_cookie('refresh_token', value=str(token))
    res.set_cookie('access_token', value=str(token.access_token))
    return res



#### view
class SignupView(APIView):
    def post(self, request):
        college=request.data.get('college')
        major=request.data.get('major')
#### 3
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            
        user_profile = UserProfile.objects.create(
            user=user,
            college=college,
            major=major
        )

        return set_token_on_response_cookie(user,user_profile)
#### 4
        #serialized_data = generate_token_in_serialized_data(user, user_profile)
#### 5
        #return Response(serialized_data, status=status.HTTP_201_CREATED)
    

class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
        except:
            return Response({"detail": "아이디 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        user_profile = UserProfile.objects.get(user=user)

        return set_token_on_response_cookie(user, user_profile)

class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RefreshView(APIView):
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
        print(request.user)
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user.id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        profile_serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if not profile_serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user

        try:
            profile = UserProfile.objects.get(user=user.id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user_serializer = UserSerializer(user, data=request.data, partial=True)

        if not user_serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer.save()

        profile_serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if not profile_serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        profile_serializer.save()
        
        return Response(profile_serializer.data, status=status.HTTP_200_OK)  
