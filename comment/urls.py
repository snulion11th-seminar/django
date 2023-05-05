from django.urls import path
from .views import CommentListView

app_name = 'comment'
urlpatterns = [
    path("", CommentListView.as_view()),
    path("<int:comment_id>/", CommentListView.as_view()),
    path("?post=<int:post_id>", CommentListView.as_view()),
]

