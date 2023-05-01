from django.urls import path, re_path
from .views import CreateCommentView, UpdateCommentView

app_name = 'comment'
urlpatterns = [
    # FBV url path
    # path("register_post/", CreatePostView, name='post'),
    # path("see_post/", ReadAllPostView, name="get"),

    path("", CreateCommentView.as_view()),  # 추가
    path("<int:comment_id>/", UpdateCommentView.as_view()),  # 추가
]
