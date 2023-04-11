from django.urls import path
from .views import ReadAllPostView, CreatePostView, UpdatePost, PostListView, PostDetailView

app_name = 'post'
urlpatterns = [
    # FBV url path
    path("register_post/", CreatePostView, name='post'),
    path("see_post/", ReadAllPostView, name="get"),
    path("update/<int:post_id>/",UpdatePost, name='patch'),
    # CBV url path
    path("", PostListView.as_view()), 
    path("<int:post_id>/", PostDetailView.as_view())
]