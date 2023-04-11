from django.urls import path
from .views import ReadAllPostView, CreatePostView, PostListView, PostDetailView

app_name = 'post'
urlpatterns = [
    path("register_post/", CreatePostView, name='post'),
    path("see_post/", ReadAllPostView, name="get"),
    path("", PostListView.as_view()),
    path("<int:post_id>/", PostDetailView.as_view())
]

