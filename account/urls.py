from django.urls import path
from .views import SignupView
from .views import SigninView, LogoutView, SignupView, UserInfoView, ProfileInfoView, TokenRefreshView


app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("signin/", SigninView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("info/", UserInfoView.as_view()),
    path("profile/", ProfileInfoView.as_view()),
]
