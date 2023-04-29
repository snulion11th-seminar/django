from django.shortcuts import render

# Create your views here.
#### 1
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer,UserProfileSerializer
#### 2
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated ##add
from rest_framework_simplejwt.authentication import JWTAuthentication ##add


def generate_token_in_serialized_data(user:User) -> UserSerializer.data:
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

#### view
class SignupView(APIView):
    def post(self, request):
        college=request.data.get('college')
        major=request.data.get('major')

#### 3
        user_serializer = UserSerializer(data=request.data)
        #request에서 data를 가져올 때는 data= 을 명시해주어야 함
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            
        user_profile = UserProfile.objects.create(
            user=user,
            college=college,
            major=major
        )
        return set_token_on_response_cookie(user)
    
    
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
        return set_token_on_response_cookie(user)
    
class LogoutView(APIView):
    def post(self, request):
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RefreshTokenView(APIView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.data['refresh_token']
        if not refresh_token:
            return Response({'error': 'No refresh token provided'}, status=400)

        #if not request.user.is_authenticated:
        #    return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = refresh_token.access_token
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=400)
        res = Response({'detail':'access_token is refreshed'}, status=200)
        res.set_cookie('access_token', value=str(access_token), httponly=True)
        return res