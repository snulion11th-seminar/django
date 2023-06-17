"""seminar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/post/', include('post.urls')),
    path('api/account/', include('account.urls')),
    path('api/tag/', include('tag.urls')),
    path('api/comment/', include('comment.urls')),
]

# url 통해서 api 에게 주기 때문에 이름을 다르게 해서 뷰를 불러야 하는데 그 이름이 url이 됨.
# 각각의 앱으로 들어가는 모든 url의 시작을 정할 수 있음.