from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from post.models import Post

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)