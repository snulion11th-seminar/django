from django.urls import path
# from .views import 
from .views import RefreshView, CookieView

app_name = 'refresh'
urlpatterns = [
    path("", RefreshView.as_view()),
    path("cookie/", CookieView.as_view()),
]
