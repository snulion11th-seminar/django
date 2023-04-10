

from django.urls import path
from .views import PostListView, PostDetailView

app_name = 'post'
urlpatterns = [

    path("", PostListView.as_view()),
    path("<int:post_id>/", PostDetailView.as_view())
]
