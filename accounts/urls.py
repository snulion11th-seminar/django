from django.urls import path
from .views import SignupView, SigninView, LogoutView

app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view(), name='signup'),
    path("signin/", SigninView.as_view(), name='signin'),
    path("logout/", LogoutView.as_view(), name='logout'),
]