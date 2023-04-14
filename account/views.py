from django.shortcuts import render

# Create your views here.
#### 1 사용해야하는 모델 시리얼라이저 임포트
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer,UserProfileSerializer
#### 2 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def generate_token_in_serialized_data(user:User, user_profile:UserProfile) -> UserSerializer.data:
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token)
    serialized_data = UserProfileSerializer(user_profile).data
    serialized_data['token']={"access":access_token, "refresh":refresh_token}
    return serialized_data

#### view 
class SignupView(APIView):
    def post(self, request):
        college=request.data.get('college') 
        major=request.data.get('major')

#### 3 
        user_serializer = UserSerializer(data=request.data) 
                        #request에서 데이터를 바로 가져올떈 데이터=을 명시해줘야함
        if user_serializer.is_valid(raise_exception=True): #갈길잃은 데이터들이 유효한지 검증해야함
            user = user_serializer.save()                #isvalid메소드를 이용!
                                                        #뭔가 잘못되면exception을 켜라!

        user_profile = UserProfile.objects.create(
            user=user,
            college=college,
            major=major #orl을 통해서만 장고의db에 접근가능 
        )
        return set_token_on_response_cookie(user)
#### 4
        # token = RefreshToken.for_user(user) 
        # #리프레쉬 토근 안에 유저 어쩌고 넣으면 토큰 발급(access랑 refresh토큰 둘다 발급!)
        # refresh_token, access_token = str(token), str(token.access_token)
        # serialized_data = UserSerializer(user).data
        # serialized_data['token']={"access":access_token, "refresh":refresh_token}
        # #이런 딕셔너리를 할당하겠다
        
class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
        except:
            return Response({"detail": "아이디 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        user_profile = UserProfile.objects.get(user=user)
        return set_token_on_response_cookie(user, user_profile)

class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class RefreshtokenView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            newAccesstoken=RefreshToken(request.COOKIES.get('refresh_token')).access_token
        except:
            return Response({"detail": "refresh_token 이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        res=Response(status=status.HTTP_200_OK)
        res.set_cookie('access_token', value=str(newAccesstoken),httponly=True)
        return res



def set_token_on_response_cookie(user: User, user_profile:UserProfile) -> Response:
    token = RefreshToken.for_user(user)
    user_profile = UserProfile.objects.get(user=user)
    user_profile_serializer = UserProfileSerializer(user_profile)
    res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
    res.set_cookie('refresh_token', value=str(token), httponly=True)
    res.set_cookie('access_token', value=str(token.access_token), httponly=True)
    return res

