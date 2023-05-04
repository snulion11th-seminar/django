from django.urls import path
from .views import CommentListView

app_name = 'comment'
urlpatterns = [
    # FBV url path
    path("", CommentListView.as_view()),
    path("<int:comment_id>/", CommentListView.as_view()), ### 추가
]