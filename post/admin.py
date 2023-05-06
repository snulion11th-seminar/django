from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Post, Like   # 추가

admin.site.register(Post)  # 추가
admin.site.register(Like)
