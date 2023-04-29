from django.urls import path
from .views import SigninView, SignupView

app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("signin/", SigninView.as_view())
]

from django.urls import path
from .views import SigninView, LogoutView, SignupView, Refresh

app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("signin/", SigninView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("refresh/",Refresh.as_view())
]
