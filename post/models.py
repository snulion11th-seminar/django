from django.db import models
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


# Create your models here.
from django.utils import timezone
class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title