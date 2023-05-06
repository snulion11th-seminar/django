from rest_framework.serializers import ModelSerializer
from account.serializers import UserIdUsernameSerializer

from post.serializers import PostSerializer

from .models import Comment

class CommentSerializer(ModelSerializer):
    author=UserIdUsernameSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"