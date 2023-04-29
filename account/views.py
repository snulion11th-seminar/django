from django.shortcuts import render
#### 1
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer,UserProfileSerializer
#### 2
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import Token

# Create your views here.

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
    res.set_cookie('refresh_token', value=str(token), httponly=True)
    res.set_cookie('access_token', value=str(token.access_token), httponly=True)
    return res

def get_refresh_token_from_cookie(request):
    refresh_token = None
    if 'refresh_token' in request.COOKIES:
        refresh_token = request.COOKIES['refresh_token']
    else:
        return Response({"detail" : "Refresh Token not exists."}, status=status.HTTP_404_NOT_FOUND)
    return refresh_token

def get_access_token_from_cookie(request):
    access_token = None
    if 'access_token' in request.COOKIES:
        access_token = request.COOKIES['access_token']
    else :
        return Response({"detail" : "Access Token not exists."}, status=status.HTTP_404_NOT_FOUND)
    return access_token


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

from rest_framework_simplejwt.tokens import AccessToken

class ReissueAccessTokenView(APIView):
    def post(self, request):
        #### part 1 : access token(in cookie) validation chech
        try :
            access_token_str = get_access_token_from_cookie(request)
            access_token = AccessToken(access_token_str)
            access_token.verify()
            return Response({"detail" : "Token is still valid"}, status=status.HTTP_200_OK)
        
        except Exception as e :
            print(f"ERROR : {e}, try reissuing access token")

            #### part 2 : get refresh token, create new access token. 
            # 2 - 1 : Get the refresh token from the cookie
            refresh_token_str = get_refresh_token_from_cookie(request)
            try: 
                # 2 - 2 : by create RefreshToken instance with token string, automatically calls token.verify()
                refresh_token = RefreshToken(refresh_token_str)
                # 2 - 3 : create new access token
                new_access_token = str(refresh_token.access_token)
                
            except Exception as e:
                print(f"Error : {e}")
                return Response({"detail" : "Token Error"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Put new access token in cookie and return Response
        res = Response({"detail": "New Access Token"}, status=status.HTTP_202_ACCEPTED)
        res.set_cookie('access_token', value=new_access_token, httponly=True)
        return res