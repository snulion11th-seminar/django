from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tag.models import Tag

class Post(models.Model):
    title = models.CharField(max_length=256) # 최대 길이 정의가 필요함.
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.localtime)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(User, blank=True, related_name='like_posts', through='Like') # like_users -> manytomanyfield 안에 user model 있음 => user-post many-to-many 로 연결.. ^^ # through -> 중계테이블
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
