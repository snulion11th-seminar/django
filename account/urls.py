from django.urls import path
from .views import SigninView, SignupView, LogoutView, ReissueAccessTokenView, UserInfoView, UserProfileView

app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("signin/", SigninView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("refresh/", ReissueAccessTokenView.as_view()),
    path("info/", UserInfoView.as_view()),
    path("info/profile/", UserProfileView.as_view()),
]