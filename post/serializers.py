from rest_framework.serializers import ModelSerializer
from .models import Post
from account.serializers import UserIdUsernameSerializer
from tag.serializers import TagSerializer

class PostSerializer(ModelSerializer):
    author = UserIdUsernameSerializer(read_only=True)
    # author field도 함께 직렬화함 
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = "__all__"