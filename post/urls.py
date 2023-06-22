from django.urls import path
from .views import PostListView, PostDetailView, LikeView, MyPostListView

app_name = 'post'
urlpatterns = [
    path("", PostListView.as_view()),
    path("<int:post_id>/", PostDetailView.as_view()),
    # 7th week(ManyToMany Field_Like)
    path("<int:post_id>/like/", LikeView.as_view()),
    path("my/", MyPostListView.as_view()),
]