from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User
from post.models import Post

###########수정
class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE) 
    #게시물의 아이디(여기선 foreign key)를 받아다가 post에 저장
    #이걸 urls.py에서 쿼리파라미터 받아올때 그대로 사용
    content = models.TextField()
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"id={self.id}, author_id={self.author.id}, content={self.content}"