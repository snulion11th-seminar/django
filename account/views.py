#### 1
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer,UserProfileSerializer
#### 2
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserProfileSerializer, UserIdUsernameSerializer
## UserIdUsernameSerializer 추가

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




#### view
class SignupView(APIView):
    def post(self, request):
        # college=request.data.get('college')
        # major=request.data.get('major')

#### 3
        user_serialier = UserSerializer(data=request.data)
        if user_serialier.is_valid(raise_exception=True):
            user = user_serialier.save()
            
        # user_profile = UserProfile.objects.create(
        #     user=user,
        #     college=college,
        #     major=major
        # )
        return set_token_on_response_cookie(user)
    

class SigninView(APIView):
    def post(self, request):
        print(request.data)
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
            print(user)
        except:
            return Response({"detail": "아이디 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        return set_token_on_response_cookie(user)
    
class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data['refresh'])
        try:
            token = RefreshToken(request.data['refresh'])
            # token.verify()
        except:
            return Response({"detail": "Wrong Refresh Token!."}, status=status.HTTP_401_UNAUTHORIZED)
        res = Response({"detail":"Access Token Refreshed"}, status=status.HTTP_200_OK)
        res.set_cookie('access_token', value=str(token.access_token))

        return res
    

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
        userProfile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(userProfile)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        user=request.user
        user_profile = UserProfile.objects.get(user=user)
        user_profile.user.email=request.data.get('email', user_profile.user.email)
        user_profile.user.username = request.data.get('username', user_profile.user.username)
        user_profile.college = request.data.get('college', user_profile.college)
        user_profile.major = request.data.get('major', user_profile.major)
        user_profile.user.save()
        user_profile.save()
        user_profile_serializer = UserProfileSerializer(user_profile)
        return Response(user_profile_serializer.data, status=status.HTTP_200_OK)