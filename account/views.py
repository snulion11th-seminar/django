from django.shortcuts import render

# Create your views here.
#### 1
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserIdUsernameSerializer
#### 2
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.models import TokenUser


from rest_framework_simplejwt.tokens import Token


def set_token_on_response_cookie(user: User) -> Response:
    token = RefreshToken.for_user(user)
    user_profile = UserProfile.objects.get(user=user)
    print('a')
    user_profile_serializer = UserProfileSerializer(user_profile)
    print('b')
    res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
    print('c')
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
        return set_token_on_response_cookie(user)
        # token = RefreshToken.for_user(user)
        # user_profile = UserProfile.objects.get(user=user)
        # user_profile_serializer = UserProfileSerializer(user_profile)
        # res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
        # res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
        # res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
        # return res


        # serialized_data = generate_token_in_serialized_data(user, user_profile)

        # return Response(serialized_data, status=status.HTTP_201_CREATED)

class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
            print(user)
        except:
            return Response({"detail": "아이디 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        # user_profile = UserProfile.objects.get(user=user)
        # serialized_data = generate_token_in_serialized_data(user, user_profile)
        # return Response(serialized_data, status=status.HTTP_200_OK)  
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
    
class ProfileInfoView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def patch(self, request):

        # content = request.data
        # # print(content)

        # if not request.user.is_authenticated:
        #     return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        # if not content:
        #     return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)


        # try:
        #     info = UserProfile.objects.get(user = request.user)

        # except:
        #     return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # # profile = UserProfile.objects.get(user=request.user)
        # serializer = UserSerializer(request.user, data=request.data, partial=True)
        
        # print(serializer)
        # if not serializer.is_valid(raise_exception=True):
        #     return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        # print('d')
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_200_OK)
    
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