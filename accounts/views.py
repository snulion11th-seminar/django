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
        try:
            assert(request.data['password1'] == request.data['password2'])
            user = User.objects.create(
                email=request.data["email"],
                username=request.data['username'],
                password=request.data['password1']
                )
            auth.login(request, user)
            serialized_data = UserSerializer(user).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":f"signup error : {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
            auth.login(request, user)
            serialized_data = UserSerializer(user).data
            return Response(serialized_data)
        except Exception as e:
            return Response({"error":f"login error : {e}"})
        
class LogoutView(APIView):
    def post(self, request):
        try:
            auth.logout(request)
            return Response({"msg":f"{request.user.username} 이 logout 되었습니다."})
        except Exception as e:
            return Response({"error":f"{e}"})
        
        
################ use jwt ###################
def generate_token_in_serialized_data(user:User) -> str:
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token)
    serialized_data = UserSerializer(user).data
    serialized_data['token']={"access":access_token, "refresh":refresh_token}
    return serialized_data

class SignupView(APIView):
    def post(self, request):
        try:
            assert(request.data['password1'] == request.data['password2'])
            user = User.objects.create(
                email=request.data["email"],
                username=request.data['username'],
                password=request.data['password1']
                )            
            serialized_data = generate_token_in_serialized_data(user)
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"signup error : {e}"})
        
class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
            serialized_data = generate_token_in_serialized_data(user)
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"login error : {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    def post(self, request):
        try:
            token = request.data['refresh']
            RefreshToken(token).blacklist()
            return Response({"msg":f"logout 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error":f"{e}"}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileUpdateView(APIView):
    def patch(self, request):
        try:
            user = request.user
            profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(profile, data=request.data) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data) 
        except Exception as e:
            return Response({"err": f"{e}"})
