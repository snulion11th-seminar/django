from django.shortcuts import render

# Create your views here.

#### 1
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer,UserProfileSerializer, UserIdUsernameSerializer
#### 2
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

#### view

def generate_token_in_serialized_data(user:User, user_profile:UserProfile) -> UserSerializer.data:
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token)
    serialized_data = UserProfileSerializer(user_profile).data
    serialized_data['token']={"access":access_token, "refresh":refresh_token}
    return serialized_data

def set_token_on_response_cookie(user: User) -> Response:
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

#### 3
        user_serialier = UserSerializer(data=request.data)
        if user_serialier.is_valid(raise_exception=True):
            user = user_serialier.save()
            
        user_profile = UserProfile.objects.create(
            user=user,
            college=college,
            major=major
        )
#### 4        
        return set_token_on_response_cookie(user)
        # token = RefreshToken.for_user(user)
        # user_profile = UserProfile.objects.get(user=user)
        # user_profile_serializer = UserProfileSerializer(user_profile)
        # res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
        # res.set_cookie('refresh_token', value=str(token), httponly=True)
        # res.set_cookie('access_token', value=str(token.access_token), httponly=True)
        # return res
#         serialized_data = generate_token_in_serialized_data(user,user_profile)
# #### 5
#         return Response(serialized_data, status=status.HTTP_201_CREATED)
    



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
        
        # user_profile = UserProfile.objects.get(user=user)
        # serialized_data = generate_token_in_serialized_data(user, user_profile)
        # return Response(serialized_data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class Refresh(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            Refresh_Token = request.COOKIES.get('Refresh_Token')            
            NewAccessToken = RefreshToken(Refresh_Token).access_token
            resp=Response({"detail": "Access Token이 재발급되었습니다."}, status=status.HTTP_202_ACCEPTED)
            resp.set_cookie('access_token', value=str(NewAccessToken))
        except:
            resp=Response({"detail": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)
        return resp
    
class UserInfoView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        serializer = UserIdUsernameSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)