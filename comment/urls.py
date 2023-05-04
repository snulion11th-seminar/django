from django.urls import path
from .views import CommentListView, CommentDetailView

app_name = 'comment'
urlpatterns = [
    path("<int:comment_id>/", CommentDetailView.as_view()),
    path("", CommentListView.as_view())
]
