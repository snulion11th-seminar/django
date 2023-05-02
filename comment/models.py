from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from post.models import Post

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post,null=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)