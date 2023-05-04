from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from post.models import Post

class Comment(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
