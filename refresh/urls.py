from django.urls import path
from .views import Token

app_name = 'account'
urlpatterns = [
    path("", Token.as_view()),
]