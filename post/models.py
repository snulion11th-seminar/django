from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User

from tag.models import Tag


class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now())
    # post_set으로 related_name으로 지정됨
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # blank -> 비어있어도 괜찮다, related_name : 반대쪽에서 참조할 때의 이름, through : 중간 테이블
    like_users = models.ManyToManyField(User, blank=True, related_name='like_posts', through='Like')
    # through 를 넣지 않음으로써 django가 자동생성
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)