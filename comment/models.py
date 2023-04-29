from django.db import models

# Create your models here.
from django.utils import timezone

class Comment(models.Model):
    author = models.CharField(max_length=64)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)