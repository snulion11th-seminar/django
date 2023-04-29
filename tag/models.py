from django.db import models

# Create your models here.
class Tag(models.Model):
    # TextField는 최대 길이를 명시하지 않아도 됨
    content = models.TextField()