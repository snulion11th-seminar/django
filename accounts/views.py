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
                username=request.data['username'],
                password=request.data['password1']
                )
            auth.login(request, user)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)
        except Exception as e:
            return Response({"error":f"{e}"})