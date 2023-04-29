from django.urls import path
from .views import ReadAllPostView, CreatePostView, UpdatePostView, ReadSpecificPostView

app_name = 'post'

urlpatterns = [
    path("register_post/", CreatePostView, name='post'),
    path("see_post/", ReadAllPostView, name="get"),
    path("update_post/<int:id>/", UpdatePostView, name="update"),
    path("see_post/<int:id>/", ReadSpecificPostView, name="get")
]
