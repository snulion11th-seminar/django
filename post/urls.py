from django.urls import path
from .views import LikeView, ReadAllPostView, CreatePostView
from .views import PostListView, PostDetailView

app_name = 'post'
urlpatterns = [
    # FBV url path
    path("register_post/", CreatePostView, name='post'),
    path("see_post/", ReadAllPostView, name="get"),
    #CBV url path
    path("", PostListView.as_view()), ### 추가
    path("<int:post_id>/", PostDetailView.as_view()), ### 추가
    path("<int:post_id>/like/", LikeView.as_view(), name="like")
]
