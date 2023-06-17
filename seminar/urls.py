from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/post/', include('post.urls')),
    path('api/account/', include('account.urls')),
    path('api/tag/', include('tag.urls')),
    path('api/comment/', include('comment.urls')),
]
