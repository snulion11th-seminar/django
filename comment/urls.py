from django.urls import path
from .views import CommentListView

urlpatterns = [
    path("", CommentListView.as_view()),
    path("<int:comment_id>/", CommentListView.as_view())
]
