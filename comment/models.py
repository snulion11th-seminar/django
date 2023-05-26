from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from django.utils import timezone


# Create your models here.
class Comment(models.Model):
    content = models.TextField()    
    created_at = models.DateTimeField(default=timezone.now)
    post= models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)