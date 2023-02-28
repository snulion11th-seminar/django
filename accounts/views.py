# accounts/views.py
from django.contrib.auth.models import User 
from django.contrib import auth 
from rest_framework.views import APIView
from rest_framework.response import Response
from serializers import UserSerializer


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
            return Response(user_serializer.data)
        except Exception as e:
            return Response({"error":f"signup error : {e}"})
        
class LoginView(APIView):
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