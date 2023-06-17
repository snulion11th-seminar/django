from django.db import models

# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ('-created_at',)