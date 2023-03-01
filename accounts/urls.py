from django.urls import path
from .views import SigninView, LogoutView, SignupView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


app_name = 'accounts'
urlpatterns = [
    # FBV url path
    path("signup/", SignupView.as_view(), name='signup'),
    path("signin/", SigninView.as_view(), name='signin'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]