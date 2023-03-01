# accounts/views.py
from django.contrib.auth.models import User 
from django.contrib import auth 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
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
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
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
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)
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
def generate_token(user:User) -> str:
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token)
    return refresh_token, access_token

class SignupView(APIView):
    def post(self, request):
        try:
            assert(request.data['password1'] == request.data['password2'])
            user = User.objects.create(
                email=request.data["email"],
                username=request.data['username'],
                password=request.data['password1']
                )            
            refresh_token, access_token = generate_token(user)
            data = UserSerializer(user).data
            data['token']={"access":access_token, "refresh":refresh_token}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"signup error : {e}"})
        
class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
            refresh_token, access_token = generate_token(user)
            data = UserSerializer(user).data
            data['token']={"access": access_token, "refresh":refresh_token}
            return Response(data, status=status.HTTP_200_OK)
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