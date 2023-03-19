from django.urls import path
from .views import TagListView, TagDeleteView

app_name = 'tag'
urlpatterns = [
    path("", TagListView.as_view()),
    path("<int:tag_id>/", TagDeleteView.as_view())
]