from django.urls import path
from .views import ReadAllPostView, CreatePostView, PostListView, PostDetailView, LikeView, MyPostListView

app_name = 'post'
urlpatterns = [
    # FBV url path - 안 씀
    path("register_post/", CreatePostView),
    path("see_post/", ReadAllPostView),

    # CBV url path - 이걸로 씀
    path("", PostListView.as_view()),
    path("<int:post_id>/", PostDetailView.as_view()),
    path("<int:post_id>/like/", LikeView.as_view()),
    path("my/", MyPostListView.as_view()),
]
