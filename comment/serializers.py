from rest_framework.serializers import ModelSerializer
from .models import Comment
from account.serializers import UserIdUsernameSerializer
from post.serializers import PostSerializer


class CommentSerializer(ModelSerializer):
    author = UserIdUsernameSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "post", "author"]
