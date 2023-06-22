from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.utils import timezone
from tag.models import Tag


class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    like_users = models.ManyToManyField(User, blank=True, related_name='like_posts', through='Like')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title
        
# 7th week(ManyToMany Field_Like)
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
