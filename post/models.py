from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from tag.models import Tag


class Post(models.Model):
    like_users = models.ManyToManyField(User, blank=True, related_name='like_posts', through='Like')
    title = models.CharField(max_length=256) #제목 길이
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title #겉으로 보보기기에에는  제목이 가장 먼먼저  보보이이게
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
