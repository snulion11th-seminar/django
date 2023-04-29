from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # 1:1로 user와 userprofile을 연결해주겠다!
    college = models.CharField(max_length=32, blank=True)
    major = models.CharField(max_length=32, blank=True)

    def __str__(self): # 출력이 될 때 어떤 정보를 보여줄지!
        return f"id={self.id}, user_id={self.user.id}, college={self.college}, major={self.major}"
    