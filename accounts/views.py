# accounts/views.py
from django.contrib.auth.models import User 
from django.contrib import auth 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
<<<<<<< Updated upstream

=======
import requests, json
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
=======
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
class SignupView(APIView):
    def post(self, request):
        try:
            assert(request.data['password1'] == request.data['password2'])
            user = User.objects.create(
                email=request.data["email"],
                username=request.data['username'],
                password=request.data['password1']
                )
            
            user_serializer = UserSerializer(user)
            url = "http://127.0.0.1:8000/api/api/token"
            response = requests.request("post",url, json=request.data)
            return Response(response.json())
        except Exception as e:
            return Response({"error":f"signup error : {e}"})
        
class SigninView(APIView):
>>>>>>> Stashed changes
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
            print(request.user)
            auth.login(request, user)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"login error : {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    def post(self, request):
        try:
            signin_username = request.user
            auth.logout(request)
            return Response({"msg":f"{signin_username} 이 logout 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error":f"{e}"}, status=status.HTTP_401_UNAUTHORIZED)