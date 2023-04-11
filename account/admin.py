from django.contrib import admin
from .models import UserProfile   # 추가

#register models
admin.site.register(UserProfile)  # 추가