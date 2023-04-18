from rest_framework.serializers import ModelSerializer

from account.serializers import UserSerializer

from .models import Comment


class CommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ["content", "author", "created_at"]