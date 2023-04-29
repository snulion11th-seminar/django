from django.urls import path
from .views import SigninView, SignupView, LogoutView, RefreshAccessTokenView

 
app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("signin/", SigninView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("refresh/", RefreshAccessTokenView.as_view()),
]