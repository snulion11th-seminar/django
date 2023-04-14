# from django.urls import path
# from .views import ReadAllPostView, CreatePostView

# app_name = 'post'
# urlpatterns = [
#     # FBV url path
#     path("register_post/", CreatePostView, name='post'),
#     path("see_post/", ReadAllPostView, name="get")
# ]

from django.urls import path
### 추가
from .views import ReadAllPostView, CreatePostView, PostListView, PostDetailView
###

app_name = 'post'
urlpatterns = [
    # FBV url path
    path("register_post/", CreatePostView),
    path("see_post/", ReadAllPostView),
    # CBV url path
    path("", PostListView.as_view()), ### 추가
    path("<int:post_id>/", PostDetailView.as_view()) ### 추가
]