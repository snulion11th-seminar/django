from rest_framework.serializers import ModelSerializer

from account.serializers import UserIdUsernameSerializer
from tag.serializers import TagSerializer

from .models import Post


class PostSerializer(ModelSerializer):
    author = UserIdUsernameSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
