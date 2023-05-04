from django.db import models

# Create your models here.
from django.db import models 
from django.utils import timezone
from django.contrib.auth.models import User

from post.models import Post

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank = True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  blank = True)
    created_at = models.DateTimeField(default=timezone.now)
    content = models.TextField(default="content")

