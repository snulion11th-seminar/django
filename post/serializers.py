from rest_framework.serializers import ModelSerializer
from .models import Post
from account.serializers import UserIdUsernameSerializer
from tag.serializers import TagSerializer

class PostSerializer(ModelSerializer): #modelserializer -> model을 자동으로 인식해서 serialize 해줍니다!
    author = UserIdUsernameSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = "__all__"

