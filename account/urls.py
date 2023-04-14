from django.urls import path
from .views import SignupView
from .views import SigninView, LogoutView, SignupView, ReissueToken


app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("signin/", SigninView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("refresh/", ReissueToken.as_view())
]