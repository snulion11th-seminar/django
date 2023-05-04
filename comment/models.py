from django.db import models
from post.models import Post
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)