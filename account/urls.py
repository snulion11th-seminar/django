from django.urls import path
from .views import SignupView,SigninView,LogoutView,RefreshTokenView


app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("signin/", SigninView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("refresh/",RefreshTokenView.as_view())
]