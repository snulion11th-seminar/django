from django.urls import path
from .views import RefreshView, SigninView, SignupView, LogoutView


app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("signin/", SigninView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("refresh/", RefreshView.as_view()),
]

