from django.urls import path
from .views import TagDetailView, TagListView

app_name = 'tag'
urlpatterns = [
    path("", TagListView.as_view()),
    path("<int:tag_id>/", TagDetailView.as_view())
]
