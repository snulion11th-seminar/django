from django.shortcuts import render

# Create your views here.
# 1
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer
# 2
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
# 3
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
# view


def generate_token_in_serialized_data(user: User, user_profile: UserProfile) -> UserSerializer.data:
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token)
    serialized_data = UserProfileSerializer(user_profile).data
    serialized_data['token'] = {
        "access": access_token, "refresh": refresh_token}
    return serialized_data


def set_token_on_response_cookie(user: User) -> Response:
    token = RefreshToken.for_user(user)
    user_profile = UserProfile.objects.get(user=user)
    user_profile_serializer = UserProfileSerializer(user_profile)
    res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
    res.set_cookie('refresh_token', value=str(token), httponly=True)
    res.set_cookie('access_token', value=str(
        token.access_token), httponly=True)
    return res


class SignupView(APIView):
    def post(self, request):
        college = request.data.get('college')
        major = request.data.get('major')

# 3
        user_serialier = UserSerializer(data=request.data)
        if user_serialier.is_valid(raise_exception=True):
            user = user_serialier.save()

        user_profile = UserProfile.objects.create(
            user=user,
            college=college,
            major=major
        )
        return set_token_on_response_cookie(user)
# 4
#         serialized_data = generate_token_in_serialized_data(user, user_profile)
# # 5
#         return Response(serialized_data, status=status.HTTP_201_CREATED)


class SigninView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data['username'],
                password=request.data['password']
            )
        except:
            return Response({"detail": "아이디 또는 비밀번호를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        return set_token_on_response_cookie(user)
        # user_profile = UserProfile.objects.get(user=user)
        # serialized_data = generate_token_in_serialized_data(user, user_profile)
        # return Response(serialized_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        RefreshToken(request.data['refresh']).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)


# def regenerate_access_token_on_response_cookie(user: User, refresh_token: RefreshToken) -> Response:
#     try:
#         refresh_token.check_exp()
#         # new_access_token = refresh_token.access_token <- 기존의 refresh_token에서부터 만들고 싶음... 이게 아닌가?
#         new_access_token = AccessToken.for_user(user)
#         res = Response({"detail": "access token regenerated"},
#                        status=status.HTTP_200_OK)
#         res.set_cookie('access_token', value=str(
#             new_access_token), httponly=True)
#         return res
#     except:
#         Response({"detail": "Refresh token expired"},
#                  status=status.HTTP_400_BAD_REQUEST)


class RefreshView(APIView):
    def post(self, request):
        # request.user를 통해 bearer를 타고 들어온 access token이 유효한지 검증한다. 딱 그것만 한다.
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 후 다시 시도해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        # 어떤 방식으로든 request를 타고온 refresh_token이 jwt상에서 유효한지 검증한다. access token과 매치한다거나 db와 매치한다거나 하지 않는다. 다른 방식이 필요할 것 같다.
        try:
            # print(refresh_token)
            # print(request.COOKIES)
            # print(request.user)
            '''
            refresh_token을 받아온 다음 RefreshToken class로 받으면서 검증까지 함. valid한지. 다만 이것은 jwt로 하는 자체 검증일 뿐이다. decode하는데 오류가 없는지 등을 검사
            어딘가에 저장된 refresh_token과 매치하거나 user와 매치하는 것이 아니다.
            refresh_token = RefreshToken(request.data['refresh_token'])
            또한 access_token을 만료시키거나 access token과 refresh_token 사이 검증이 필요할 것이기도 하다. 지금은 어디에도 refresh_token과 access_token이 저장되어 있지 않다.
            처음 발급할 때 response의 cookie에 태워 보내는 것으로 가장 마지막의 token이 client의 브라우저에 남아있을 뿐이다. 따라서 검증은 어디에서도 하고 있지 않다.
            '''
            # refresh_token = request.data.get("refresh_token")
            refresh_token = RefreshToken(request.COOKIES.get("refresh_token"))
            new_access_token = refresh_token.access_token
            res = Response({"detail": "access token regenerated"},
                           status=status.HTTP_200_OK)
            res.set_cookie('access_token', value=str(
                new_access_token), httponly=True)
            return res
        except TokenError as e:
            raise TokenError("Token is invalid or expired")
