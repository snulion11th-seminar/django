from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

def set_token_on_response_cookie(user: User) -> Response:
    token = RefreshToken.for_user(user)
    res = Response(f"Access Token: {str(token.access_token)}", status=status.HTTP_200_OK)
    res.set_cookie('access_token', value=str(token.access_token), httponly=True)
    return res

    
class Token(APIView):
    def get(self, request):
        return Response("!!")
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
        except:
            return Response({"detail": "아이디 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        return set_token_on_response_cookie(user)