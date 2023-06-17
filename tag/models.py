from django.db import models

# Create your models here.
class Tag(models.Model):
    content = models.TextField()
    def __str__(self):
        return self.content