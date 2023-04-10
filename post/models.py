from django.db import models

# Create your models here.
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    last_update= models.DateTimeField(auto_now=True);

    def __str__(self):
        return self.title
    
