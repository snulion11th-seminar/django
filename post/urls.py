from django.urls import path
from .views import ReadAllPostView, CreatePostView, PostListView, PostDetailView

app_name = 'post'
urlpatterns = [
    # FBV url path
    path("register_post/", CreatePostView, name='post'),
    path("see_post/", ReadAllPostView, name="get"),
    path("", PostListView.as_view()), ### 추가
    path("<int:post_id>/", PostDetailView.as_view()), ### 추가
   ## path("update_post/", UpdatePostView, name='update')
]
