from django.db import models
from post.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Comment(models.Model):
  content = models.TextField()
  created_at = models.DateTimeField(default=timezone.now)
  author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
  post = models.ForeignKey(Post,null=True, on_delete=models.CASCADE)

