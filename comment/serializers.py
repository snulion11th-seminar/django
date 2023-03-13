from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserSerializer
from django.contrib.auth.models import User

from .models import Comment


class CommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ["content", "author", "created_at"]