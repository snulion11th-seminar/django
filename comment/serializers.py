from pkgutil import read_code
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from account.serializers import UserIdUsernameSerializer
from .models import Comment

class CommentSerializer(ModelSerializer):
    author = UserIdUsernameSerializer(read_only=True)
    post = ReadOnlyField(source="post.id")

    class Meta:
        model = Comment
        fields = "__all__"