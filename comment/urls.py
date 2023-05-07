from django.urls import path
from .views import CommentListView
from .views import CommentDetailView

app_name = 'comment'
urlpatterns = [
    path("", CommentListView.as_view()),
    path("<int:comment_id>/", CommentDetailView.as_view()),
    ]