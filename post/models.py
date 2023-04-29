from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils import timezone

from tag.models import Tag

class Post(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    last_update= models.DateTimeField(auto_now=True);
    like_users=models.ManyToManyField(User, related_name="like_posts", blank=True, through='Like')
    tags=models.ManyToManyField(Tag, related_name="posts", blank=True)
    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)