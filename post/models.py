from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from tag.models import Tag

class Post(models.Model):

    like_users = models.ManyToManyField(User, blank=True, related_name='like_posts', through='Like')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    

    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

