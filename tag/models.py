from django.db import models

class Tag(models.Model):
    content = models.TextField()