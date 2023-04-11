from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile   # 추가

admin.site.register(UserProfile)  # 추가