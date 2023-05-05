from django.urls import path
from .views import CommentCreateView, CommentDetailView

app_name = 'post'
urlpatterns = [
  path("", CommentCreateView.as_view()),
  path("<int:comment_id>/",CommentDetailView.as_view()),
]