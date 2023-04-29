from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer): #modelserializer -> model을 자동으로 인식해서 serialize 해줍니다!
    class Meta:
        model = Post
        fields = "__all__"