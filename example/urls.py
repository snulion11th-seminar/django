from django.urls import path
from .views import ReadAllPostView, CreatePostView

app_name = 'example'
urlpatterns = [
    # FBV url path
    path("register_example/", CreatePostView, name='post'),
    path("see_example/", ReadAllPostView, name="get")
]