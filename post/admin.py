from django.contrib import admin

# Register your models here.
from .models import Post, Like   # 추가

admin.site.register(Post) 
admin.site.register(Like)
