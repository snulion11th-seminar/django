from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework import status

from django.contrib.auth.models import User
import datetime

class RefreshView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
                return Response({"detail": "로그인 후 다시 시도해주세요."},  status=status.HTTP_401_UNAUTHORIZE)
        try: 
            refresh_tokmanen = RefreshToken(request.COOKIES.get('refresh_token'))
            refresh_token.verify() # refresh token이 유효한지 확인
        except:
            return Response({"detail": "refresh token이 유효하지 않습니다. 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        new_access_token=str(refresh_token.access_token)
        res = Response({"access token 재발급 완료"})
        res.set_cookie('access_token', value=new_access_token, httponly=True) # 재발급한 access token 
        return res
    
class CookieView(APIView):
    def get(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        access_token = request.COOKIES.get('access_token')
        res = Response({"Token 확인 완료"})
        res.set_cookie('refresh_token', value=refresh_token, httponly=True)
        res.set_cookie('access_token', value=access_token, httponly=True)   
        return res
    

# class RefreshView(APIView):
#     def post(self, request):
#         # if not request.user.is_authenticated:
#         #         return Response({"detail": "로그인 후 다시 시도해주세요."},  status=status.HTTP_401_UNAUTHORIZE)
#         try: 
#             refresh_token = request.data['refresh']
#             refresh_token.verify()
#         except:
#             return Response({"detail": "refresh token이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
#         # refresh_token.access_token.lifetime = datetime.timedelta(seconds=0)
#         new_token=RefreshToken(refresh_token).access_token
#         res = Response({"access token 재발급 완료"})
#         res.set_cookie('access_token', value=new_token, httponly=True)
#         return res