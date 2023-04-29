from django.db import models

# Create your models here.
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=256) # 최대 길이 정의가 필요함.
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.localtime)

    def __str__(self):
        return self.title
    