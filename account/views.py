# accounts/views.py
from django.contrib.auth.models import User 
from django.contrib import auth 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,UserProfileSerializer
from .models import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken

############## no jwt ###################
class SignupView(APIView):
    def post(self, request):
        assert(request.data['password1'] == request.data['password2'])
        user = User.objects.create(
            email=request.data["email"],
            username=request.data['username'],
            password=request.data['password1']
            )
        auth.login(request, user)
        serialized_data = UserSerializer(user).data
        return Response(serialized_data, status=status.HTTP_201_CREATED)
        
class SigninView(APIView):
    def post(self, request):
        user = User.objects.get(
            username=request.data['username'],
            password=request.data['password']
        )
        auth.login(request, user)
        serialized_data = UserSerializer(user).data
        return Response(serialized_data)
        
class LogoutView(APIView):
    def post(self, request):
        auth.logout(request)
        return Response({"msg":f"{request.user.username} 이 logout 되었습니다."})
        
        
################ use jwt ###################
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
        if email and username and password:
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
        else:
            return Response({"detail": "[email, password, username] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        
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
        try:
            token = request.data['refresh']
        except:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(token).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileUpdateView(APIView):
    def patch(self, request):
        user = request.user
        profile = UserProfile.objects.filter(user=user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


        