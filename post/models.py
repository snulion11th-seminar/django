from django.db import models
# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from tag.models import Tag

class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(User, blank=True, related_name='like_posts', through='Like')
    # 'User' 테이블에 있는 primary key를 참조하겠다는 뜻.
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title