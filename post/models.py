from django.db import models

# Create your models here.
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=256) #제목 길이
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title #겉으로 보보기기에에는  제목이 가장 먼먼저  보보이이게
    
